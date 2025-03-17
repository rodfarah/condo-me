from apps.condo.models import SetupProgress
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
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
    'Setup Area' View is associated with the main 'condominium setup page', where manager
    user may configure the condominium itself, blocks, apartments, common areas,
    caretakers and residents.
    """

    template_name = "condo/pages/setup_pages/setup_main/condo_setup_home.html"

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
