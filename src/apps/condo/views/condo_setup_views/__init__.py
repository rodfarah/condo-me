# flake8: noqa
from .base import (
    SetupAreaView,
    SetupProgressMixin,
    SetupViewsWithDecors,
    manager_group_required,
)
from .setup_apartment_views import (
    SetupApartmentCreateView,
    SetupApartmentDeleteView,
    SetupApartmentEditView,
    SetupApartmentMultipleCreateView,
    SetupApartmentsByBlockListView,
)
from .setup_block_views import (
    SetupBlockCreateView,
    SetupBlockDeleteView,
    SetupBlockEditView,
    SetupBlockListView,
)
from .setup_common_area_views import SetupCommonAreaCreateView, SetupCommonAreaListView
from .setup_condominium_views import SetupCondominiumView
