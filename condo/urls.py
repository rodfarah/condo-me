from django.urls import path

from condo import views

app_name = "condo"

urlpatterns = [
    path("", views.home, name="home"),
    path("condominium/", views.condominium, name="condominium"),
    path("condominium/setup/", views.condominium_setup, name="condominium_setup"),
    path("condominium/common_areas/", views.common_areas, name="common_areas"),
    path(
        "user/profile/settings/",
        views.user_profile_settings,
        name="user_profile_settings",
    ),
]
