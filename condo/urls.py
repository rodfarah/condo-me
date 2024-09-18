from django.urls import path

from condo import views

app_name = "condo"

urlpatterns = [
    path("", views.home, name="home"),
    path("setup-area/condominium", views.setup_condominium, name="setup_condominium"),
    # path("setup-area/blocks", views.setup_blocks, name="setup_blocks"),
    # path("setup-area/apartments", views.setup_apartments, name="setup_apartments"),
    # path(
    #     "setup-area/common-areas", views.setup_common_areas, name="setup_common_areas"
    # ),
    path("setup-area", views.setup_area, name="setup_area"),
    path("condominium/common_areas/", views.common_areas, name="common_areas"),
    path("condominium/", views.condominium, name="condominium"),
    path(
        "user/profile/settings/",
        views.user_profile_settings,
        name="user_profile_settings",
    ),
]
