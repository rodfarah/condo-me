from django.contrib import admin
from .models import Condominium, Block, Apartment, CommonArea

# Register models into admin interface:


@admin.register(Condominium)
class CondominiumAdmin(admin.ModelAdmin):
    ...


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    ...


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    ...


@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    ...
