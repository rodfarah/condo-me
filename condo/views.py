from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.shortcuts import render


def manager_group_required(view_func):
    """
    This decorator checks if user belongs to 'manager' group
    """

    def check_group(user):
        if user.groups.filter(name="manager").exists():
            return True
        raise Http404("You don't have manager permissions to access this page.")

    return user_passes_test(check_group)(view_func)


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
@manager_group_required
def setup_area(request):
    return render(request, template_name="condo/pages/setup_pages/setup_area.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def home(request):
    return render(request, template_name="condo/pages/home.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def condominium(request):
    return render(request, template_name="condo/pages/condominium.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def common_areas(request):
    return render(request, "condo/pages/common_areas.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def user_profile_settings(request):
    return render(request, "condo/pages/user_profile.html")
