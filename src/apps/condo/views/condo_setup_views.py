from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, UpdateView

from apps.condo.forms import BlockSetupForm, CondoSetupForm
from apps.condo.models import Block, Condominium


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


class SetupAreaView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/condo_setup_home.html"

    def get(self, request):
        user_has_condo = getattr(request.user, "condominium", None)
        if user_has_condo:
            return render(
                request,
                self.template_name,
                context={"condo_cover": request.user.condominium.cover.name},
            )
        return render(request, self.template_name)


class SetupCondominiumView(SetupViewsWithDecors, UpdateView):
    model = Condominium
    template_name = "condo/pages/setup_pages/condo_setup_condominium.html"
    form_class = CondoSetupForm
    success_url = reverse_lazy("condo:condo_setup_condominium")

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
        #  "self.object" is the instance of "get_object()", the user condominium itself
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
        context["condo_exists"] = bool(self.object)  # True or False
        return context

    def form_valid(self, form):
        """
        Called when a valid form data has been POSTED.
        Associates the condominium with the current user and saves both.
        """
        self.object = form.save()
        # user has just created his own condominium, so ...
        self.request.user.condominium = self.object
        self.request.user.save()
        messages.success(self.request, "Condominium successfully created or updated!")
        return super().form_valid(form)


class SetupBlockListView(SetupViewsWithDecors, ListView):
    """
    This class generates a list of blocks of the user condominium.
    """

    model = Block
    http_method_names = ["get"]
    template_name = "condo/pages/setup_pages/condo_setup_blocks.html"

    def get_queryset(self):
        return Block.objects.filter(condominium=self.request.user.condominium)


class SetupBlockView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/condo_setup_block.html"

    def get(self, request, block_id=None):
        user_condominium = request.user.condominium
        # If template sends block_id, get method. Otherwise, user wants to create new block.
        if block_id:
            # Check if block belongs to user condominium. User is authorized to get block?
            current_block = Block.objects.filter(
                condominium=user_condominium,
                id=block_id,
            ).first()
            if not current_block:
                raise PermissionDenied("Permission Denied")
            # authorized user. Send form with current block to frontend
            form = BlockSetupForm(instance=current_block)
        else:
            # no block_id means user wants to create new block
            form = BlockSetupForm()

        return render(
            request=request, template_name=self.template_name, context={"form": form}
        )
