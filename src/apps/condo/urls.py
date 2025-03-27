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
        "condo-setup/home/",
        condo_setup_views.base.SetupAreaView.as_view(),
        name="condo_setup_home",
    ),
    ########### CONDOMINIUM ###########
    path(
        "condo-setup/condominium/",
        condo_setup_views.setup_condominium_views.SetupCondominiumView.as_view(),
        name="condo_setup_condominium",
    ),
    ########### BLOCK ###########
    path(
        "condo-setup/block-list/",
        condo_setup_views.setup_block_views.SetupBlockListView.as_view(),
        name="condo_setup_block_list",
    ),
    path(
        "condo-setup/block/create/",
        condo_setup_views.setup_block_views.SetupBlockCreateView.as_view(),
        name="condo_setup_block_create",
    ),
    path(
        "condo-setup/block/edit/<uuid:block_id>/",
        condo_setup_views.setup_block_views.SetupBlockEditView.as_view(),
        name="condo_setup_block_edit",
    ),
    path(
        "condo-setup/block/delete/<uuid:block_id>/",
        condo_setup_views.setup_block_views.SetupBlockDeleteView.as_view(),
        name="condo_setup_block_delete",
    ),
    path(
        "condo-setup/blocks-to-apartments/",
        condo_setup_views.setup_block_views.SetupBlockListView.as_view(
            template_purpose="apartments"
        ),
        name="condo_setup_blocks_to_apartments",
    ),
    ########### APARTMENT ###########
    path(
        "condo-setup/block/<uuid:block_id>/apartments/",
        condo_setup_views.setup_apartment_views.SetupApartmentsByBlockListView.as_view(),
        name="condo_setup_apartment_list_by_block",
    ),
    path(
        "condo-setup/block/<uuid:block_id>/apartments/create/",
        condo_setup_views.setup_apartment_views.SetupApartmentCreateView.as_view(),
        name="condo_setup_apartment_create",
    ),
    path(
        "condo-setup/block/<uuid:block_id>/apartments/create/multiple/",
        condo_setup_views.setup_apartment_views.SetupApartmentMultipleCreateView.as_view(),
        name="condo_setup_apartment_multiple_create",
    ),
    path(
        "condo-setup/apartments/<uuid:apartment_id>/edit/",
        condo_setup_views.setup_apartment_views.SetupApartmentEditView.as_view(),
        name="condo_setup_apartment_edit",
    ),
    path(
        "condo-setup/apartments/<uuid:apartment_id>/delete/",
        condo_setup_views.setup_apartment_views.SetupApartmentDeleteView.as_view(),
        name="condo_setup_apartment_delete",
    ),
    ########### COMMON AREA ###########
    path(
        "condo-setup/common-areas/list/",
        condo_setup_views.setup_common_area_views.SetupCommonAreaListView.as_view(),
        name="condo_setup_common_area_list",
    ),
    path(
        "condo-setup/common-areas/create/",
        condo_setup_views.setup_common_area_views.SetupCommonAreaCreateView.as_view(),
        name="condo_setup_common_area_create",
    ),
    path(
        "condo-setup/common-areas/<uuid:common_area_id>/edit/",
        condo_setup_views.setup_common_area_views.SetupCommonAreaEditView.as_view(),
        name="condo_setup_common_area_edit",
    ),
    path(
        "condo-setup/common-areas/<uuid:common_area_id>/delete/",
        condo_setup_views.setup_common_area_views.SetupCommonAreaDeleteView.as_view(),
        name="condo_setup_common_area_delete",
    ),
]
