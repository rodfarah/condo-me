from django.contrib import admin
from .models import Condominium, Block, Apartment, CommonArea

# change Django Administrator (title)
admin.site.site_header = "Condo-me - Admin Panel"


# Register models into admin interface:


@admin.register(Condominium)
class CondominiumAdmin(admin.ModelAdmin):
    ...


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    ...


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    list_display = ["number", "block"]
    search_fields = ["number"]


@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    readonly_fields = ["maximum_using_time"]
