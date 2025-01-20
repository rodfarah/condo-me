from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView

from apps.condo.forms import BlockSetupForm, CondoSetupForm
from apps.condo.models import Block, Condominium, SetupProgress


# Create a 'manager group required' decorator
def manager_group_required(view_func):
    """
    This decorator checks if user belongs to 'manager' group.
    Redirects to the login page if the user does not belong to this group
    """

    def check_group(user):
        if user.groups.filter(name="manager").exists():
            return True
        raise PermissionDenied("You do not have the required permissions")

    return user_passes_test(
        test_func=check_group,
        login_url="/condo_people/login",
        redirect_field_name="redirect_to",
    )(view_func)


# Create a class that applies login_required and manager_group_required decorators
class SetupViewsWithDecors(View):
    """
    Ensures that only logged-in users who belong to the 'manager' group can access
    setup views.
    """

    @method_decorator(
        login_required(
            redirect_field_name="redirect_to", login_url="/condo_people/login"
        )
    )
    @method_decorator(manager_group_required)
    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch method is overridden to add the manager_group_required decorator,
        ensuring that the group check occurs before anything else in the view.
        """
        return super().dispatch(request, *args, **kwargs)


class SetupProgressMixin:
    """
    Mixin to easily access and update condominium setup progress in views
    """

    def get_setup_progress(self):
        if not hasattr(self.request.user, "condominium"):
            return None

        return SetupProgress.objects.get_or_create(
            condominium=self.request.user.condominium
        )[0]

    def update_setup_progress(self):
        setup_progress = self.get_setup_progress()
        if setup_progress is not None:
            setup_progress.update_status()


class SetupAreaView(SetupViewsWithDecors):
    """
    Setup Area View is associated with the main 'condominium setup page', where manager
    user may configure the condominium itself, blocks, apartments, common areas,
    caretakers and residents.
    """

    template_name = "condo/pages/setup_pages/condo_setup_home.html"

    def get(self, request):
        condominium = getattr(request.user, "condominium", None)
        context = {}

        if not condominium:
            context.update(
                {
                    "condo_exists": False,
                    "condo_cover": None,
                    "block_exists": False,
                    "apartment_exists": False,
                    "common_area_exists": False,
                    "setup_percentage": 0,
                    "next_step": None,
                    "is_setup_complete": False,
                }
            )
        else:
            # first, we get or create the "SetupProgress" object
            setup_progress, true_or_false = SetupProgress.objects.get_or_create(
                condominium=request.user.condominium
            )
            setup_progress.update_status()
            # then we add context variables to be sent to template
            context.update(
                {
                    "condo_exists": True,
                    "condo_cover": (
                        condominium.cover.name if condominium.cover else None
                    ),  # condominium cover url
                    "block_exists": condominium.blocks.exists(),
                    "apartment_exists": condominium.apartments.exists(),
                    "common_area_exists": condominium.common_areas.exists(),
                    "setup_percentage": setup_progress.setup_percentage,
                    "next_step": setup_progress.next_step,
                    "is_setup_complete": setup_progress.setup_percentage == 100,
                }
            )
        return render(
            request,
            self.template_name,
            context=context,
        )


class SetupCondominiumView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    model = Condominium
    template_name = "condo/pages/setup_pages/condo_setup_condominium.html"
    form_class = CondoSetupForm
    success_url = reverse_lazy("condo:condo_setup_home")

    def get_object(self, queryset=None):
        """
        This function subscribes get_object method and gets the
        "user condominium" object
        """
        return self.request.user.condominium

    def get_form(self, form_class=None):
        """
        Customizes the form by making fields readonly if a condominium already exists.
        This prevents direct editing of fields unless through the 'Edit' buttons.
        """
        form = super().get_form(form_class)
        #  "self.object" is the instance of "get_object()", the current condominium itself
        if self.object:
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True
        return form

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template.
        The 'condo_exists' flag helps the template determine whether to show
        creation or editing interfaces.
        """
        context = super().get_context_data(**kwargs)
        # check if condominium exists
        condominium = self.object
        if not condominium:
            context.update(
                {
                    "condo_exists": False,
                    "condo_cover": None,
                    "block_exists": False,
                    "apartment_exists": False,
                    "common_area_exists": False,
                }
            )
        else:
            related_objects = (
                condominium.blocks.exists(),
                condominium.apartments.exists(),
                condominium.common_areas.exists(),
            )
            # template needs all context elements, not only "condo_exists"
            context.update(
                {
                    "condo_exists": bool(condominium),
                    "condo_cover": getattr(condominium, "cover", None),
                    "block_exists": related_objects[0],
                    "apartment_exists": related_objects[1],
                    "common_area_exists": related_objects[2],
                }
            )

        return context

    def form_valid(self, form):
        """
        Called when a valid form data has been POSTed.
        Associates the condominium with the current user, creates initial setup
        progress and saves everything.
        """
        # If there is not a condominium object in form (new condominium)
        it_is_new_condo = not self.object

        # Save form first.
        # form_valid() returns HttpResponseRedirect (post > redirect > get)
        success_redirect = super().form_valid(form)
        condominium_instance = form.instance

        if it_is_new_condo:
            # Associate user with new condominium
            self.request.user.condominium = condominium_instance
            self.request.user.save()

            # Add user as condo_person
            current_user = get_user_model()
            current_user.objects.filter(id=self.request.user.id).update(
                condominium=condominium_instance
            )
        message = (
            "Condominium has been created successfully"
            if it_is_new_condo
            else "Condominium has been edited successfully"
        )
        messages.success(self.request, message)
        self.update_setup_progress()
        return success_redirect


class SetupBlockListView(SetupViewsWithDecors, ListView):
    """
    This class generates a list of blocks of the user condominium.
    """

    model = Block
    http_method_names = ["get"]
    template_name = "condo/pages/setup_pages/condo_setup_blocks.html"

    def get_queryset(self):
        return Block.objects.filter(condominium=self.request.user.condominium)


class SetupBlockView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    """
    This class is responsible for creating, reading and updating a block object.
    Please, notice there are two different URLs that lead to this View:
        "condo-setup/block/create"  ==> User wants to create a new block
        "condo-setup/block/edit/<uuid:block_id>" ==> User wants to edit a specific block
    Validation is important here:
        - User must create a condominium at first in order to create/edit a block;
        - If there is a block uuid pk in url: if exists, the block must belong to
          user's condominium. Otherwise, user is unauthorized.
    """

    http_method_names = ["get", "post"]
    model = Block
    template_name = "condo/pages/setup_pages/condo_setup_block.html"
    form_class = BlockSetupForm
    pk_url_kwarg = "block_id"  # to help get_object() method find uuid block pk from url
    success_url = reverse_lazy("condo:condo_setup_block_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.condominium:
            messages.error(
                request,
                "In order to create or edit a block, you must create a condominium first.",
            )
            return redirect("condo:condo_setup_condominium")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return a general queryset (not a single object) filtered by user's condominium.
        The single object will be obtained later, using get_object() method.
        """
        return Block.objects.filter(condominium=self.request.user.condominium)

    def get_object(self, queryset=None):
        # url may contain a uuid pk ("condo-setup/block/edit/<uuid:block_id>")
        block_id = self.kwargs.get("block_id")

        if (
            block_id is None
        ):  # it is a new block to be created ("condo-setup/block/create")
            return None  # no object to be edited
        if (
            queryset is None
        ):  # no blocks created for the condominium yet (condo-setup/block/edit/<uuid:block_id>)
            queryset = self.get_queryset()
        try:
            current_block = queryset.get(pk=block_id)
            return current_block
        except Block.DoesNotExist:
            messages.error(
                self.request,
                "This block does not exist or you do not have permission to edit it",
            )
            return None

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template.
        The 'condo_exists' flag helps the template determine whether to show
        creation or editing interfaces.
        """
        context = super().get_context_data(**kwargs)
        context["block_exists"] = bool(self.object)  # self.object == get_object()
        if self.object:
            context["block_id"] = self.object.id
        return context

    def form_valid(self, form):
        """
        This method is called after the form is validated successfully.
        Ensure new block will be associated to the current condominium.
        """

        # get form instance without saving it
        self.object = form.save(commit=False)

        # make sure user's condominium is associated to block
        self.object.condominium = self.request.user.condominium

        # save new block
        self.object.save()
        self.update_setup_progress()

        messages.success(self.request, "Block has been created or edited successfully")
        return HttpResponseRedirect(self.get_success_url())


class SetupBlockDeleteView(SetupViewsWithDecors, DeleteView, SetupProgressMixin):
    model = Block
    template_name = "condo/pages/setup_pages/condo_setup_block_delete.html"
    success_url = reverse_lazy("condo:condo_setup_block_list")
    pk_url_kwarg = "block_id"

    def get_context_data(self, **kwargs):
        """Send block_id and block_name to template"""
        context = super().get_context_data(**kwargs)
        block_id = self.kwargs.get("block_id")
        block = Block.objects.filter(pk=block_id).first()
        context["block_id"] = block_id
        context["block_name"] = block.name
        return context
