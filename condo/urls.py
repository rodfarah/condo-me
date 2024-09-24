from django.urls import path

from condo.views import condo_base_views, setup_area_views

app_name = "condo"

urlpatterns = [
    path("", condo_base_views.home, name="home"),
    path(
        "setup-area/condominium",
        setup_area_views.SetupCondominiumView.as_view(),
        name="setup_condominium",
    ),
    # path("setup-area/blocks", views.setup_blocks, name="setup_blocks"),
    # path("setup-area/apartments", views.setup_apartments, name="setup_apartments"),
    # path(
    #     "setup-area/common-areas", views.setup_common_areas, name="setup_common_areas"
    # ),
    path("setup-area/", setup_area_views.SetupAreaView.as_view(), name="setup_area"),
    path(
        "condominium/common_areas/", condo_base_views.common_areas, name="common_areas"
    ),
    path("condominium/", condo_base_views.condominium, name="condominium"),
    path(
        "user/profile/settings/",
        condo_base_views.user_profile_settings,
        name="user_profile_settings",
    ),
]
