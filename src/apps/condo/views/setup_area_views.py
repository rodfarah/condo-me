from apps.condo.forms import CondoSetupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View


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
    template_name = "condo/pages/setup_pages/setup_area.html"

    def get(self, request):
        user_has_condo = getattr(request.user, "condominium", None)
        if user_has_condo:
            return render(
                request,
                self.template_name,
                context={"condo_cover": request.user.condominium.cover.name},
            )
        return render(request, self.template_name)


class SetupCondominiumView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/setup_condominium.html"

    def get(self, request):
        # Check if user is associated to a specific condominium
        condominium = getattr(request.user, "condominium", None)
        if condominium is None:
            condo_exists = False
            form = CondoSetupForm()  # empty form to be filled in by user
        else:
            # Send condominium data to form if condominium already exists
            form = CondoSetupForm(instance=condominium)
            condo_exists = True
            # transform form as read only
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True

        return render(
            request,
            self.template_name,
            context={"form": form, "condo_exists": condo_exists},
        )

    def post(self, request):
        # check if user is alredy associated to a condominium
        user_condominium = getattr(request.user, "condominium", None)

        if user_condominium is None:
            # then, user is posting a condominium for the first time
            form = CondoSetupForm(data=request.POST, files=request.FILES or None)

        else:
            # user is editing some condominium fields
            form = CondoSetupForm(
                data=request.POST,
                files=request.FILES or None,
                instance=user_condominium,  # in order to keep unaltered fields
            )
        if form.is_valid():
            new_condominium = form.save()
            # Associates condominium to this specific user
            request.user.condominium = new_condominium
            request.user.save()
            messages.success(
                request,
                "Condominium has been successfully created or edited.",
            )
            return redirect("apps.condo:setup_condominium")
        return render(
            request,
            self.template_name,
            context={"form": form, "condo_exists": True},
        )
