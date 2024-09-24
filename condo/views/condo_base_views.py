from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def home(request):
    # send condominum cover path to be rendered in welcome page
    if request.user.condominium:
        return render(
            request,
            template_name="condo/pages/home.html",
            context={"condo_cover": request.user.condominium.cover.name},
        )
    # if not condominium, no need to send condo cover. Template will use a standard one
    return render(request, "condo/pages/home.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def condominium(request):
    return render(request, template_name="condo/pages/condominium.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def common_areas(request):
    return render(request, "condo/pages/common_areas.html")


@login_required(redirect_field_name="redirect_to", login_url="/condo_people/login")
def user_profile_settings(request):
    return render(request, "condo/pages/user_profile.html")