from django.urls import path

from .views import condo_base_views, condo_setup_views

app_name = "condo"

urlpatterns = [
    # CONDO BASE (first page user gets as soon as logs in)
    path("", condo_base_views.home, name="home"),
    path("condominium/", condo_base_views.condominium, name="condominium"),
    path(
        "user/profile/settings/",
        condo_base_views.user_profile_settings,
        name="user_profile_settings",
    ),
    path("common_areas/", condo_base_views.common_areas, name="common_areas"),
    # CONDO SETUP (only 'manager' group users have access to condo setup)
    path(
        "condo-setup/home",
        condo_setup_views.SetupAreaView.as_view(),
        name="condo_setup_home",
    ),
    path(
        "condo-setup/condominium/",
        condo_setup_views.SetupCondominiumView.as_view(),
        name="condo_setup_condominium",
    ),
    path(
        "condo-setup/blocks/",
        condo_setup_views.SetupBlocksView.as_view(),
        name="condo_setup_blocks",
    ),
    # path("condo-setup/apartments/", views.setup_apartments, name="setup_apartments"),
    # path(
    #     "condo-setup/common-areas/", views.setup_common_areas, name="setup_common_areas"
    # ),
]
