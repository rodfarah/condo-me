from typing import Any

from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest

from apps.condo.models import Apartment, Block, CommonArea, Condominium

# change Django Administrator (title)
admin.site.site_header = "Condo-me - Admin Panel"


# Register models into admin interface:


@admin.register(Condominium)
class CondominiumAdmin(admin.ModelAdmin): ...


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin): ...


@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    readonly_fields = ["maximum_using_time"]


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    list_display = ["number_or_name", "block", "condominium"]
    search_fields = ["number_or_name"]
    # Items to be shown as you choose one apartment
    fields = [
        "condominium",
        "number_or_name",
        "block",
        "display_residents",
    ]
    readonly_fields = ["display_residents"]

    def display_residents(self, obj):
        return obj.get_residents()

    display_residents.short_description = "Residents"

    # TODO: This is WRONG and needs to be fixed!
    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField | None:
        if db_field.name == "block":
            if request.POST.get("condominium"):
                kwargs["queryset"] = Block.objects.filter(
                    condominium_id=request.POST.get("condominium")
                )
            elif request.GET.get("condominium"):
                kwargs["queryset"] = Block.objects.filter(
                    condominium_id=request.GET.get("condominium")
                )
            else:
                kwargs["queryset"] = Block.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
