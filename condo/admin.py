from django.contrib import admin
from .models import Condominium, Block, Apartment, CommonArea

# Register models into admin interface:


class CondominiumAdmin(admin.ModelAdmin):
    ...


class BlockAdmin(admin.ModelAdmin):
    ...


admin.site.register(Condominium, CondominiumAdmin)
admin.site.register(Block, BlockAdmin)

# There is another (similar) way to register models into admin interface:


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    ...


@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    ...
