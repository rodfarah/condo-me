from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView

from apps.condo.forms import BlockSetupForm, CondoSetupForm
from apps.condo.models import Condominium


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
    This class applies both login_required and manager_group_required
    decorators to all setup area CBVs (following DRY principle).
    Ensures that only logged-in users who belong to the 'manager' group can access these views.
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
    success_url = reverse_lazy("apps.condo:condo_setup_condominium")

    def get_object(self, queryset=None):
        return self.request.user.condominium

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object:  #  self.object calls get_object()
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["condo_exists"] = bool(self.object)
        return context

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            self.object = form.save()

            messages.success(request, "Condominium successfully updated.")
            return redirect(self.get_success_url())
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating condominium")
        return render(
            self.request, self.template_name, {"form": form, "condo_exists": True}
        )

    def form_valid(self, form):
        self.object = form.save()
        # user has just created his own condominium, so ...
        self.request.user.condominium = self.object
        self.request.user.save()
        messages.success(self.request, "Condominium successfully created or updated!")
        return super().form_valid(form)


class SetupBlocksView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/condo_setup_blocks.html"

    def get(self, request):
        # Check if there is a condominium associated with registered user
        condominium = getattr(request.user, "condominium", None)
        if condominium is None:
            condo_exists = False
        else:
            condo_exists = True
            # Check if there are block(s) associated to the condominium
            blocks = condominium.blocks.all()
            if not blocks.exists():
                block_exists = False
                form = BlockSetupForm()  # empty form to be filled in by user
            else:
                # Send block(s) data to form if block(s) already exist(s)
                block_exists = True
                form = None
                # transform form as read only (click on edit button)
                # for field in form.fields.values():
                #     field.widget.attrs["readonly"] = True
        return render(
            request,
            self.template_name,
            context={
                "form": form,
                "condo_exists": condo_exists,
                "block_exists": block_exists,
                "blocks": blocks,
            },
        )

    def post(self, request):
        pass
        pass
