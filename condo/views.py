from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def home(request):
    return render(request=request, template_name="condo/pages/home.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def condominium(request):
    return render(request=request, template_name="condo/pages/condominium.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def common_areas(request):
    return render(request, "condo/pages/common_areas.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def user_profile_settings(request):
    return render(request, "condo/pages/user_profile.html")
