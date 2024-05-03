from django.contrib import admin
from .models import Manager, Caretaker, Resident


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    search_fields = ("name",)
    exclude = ["name", ]


@admin.register(Caretaker)
class CaretakerAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    search_fields = ("name",)
    exclude = ["name", ]


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    search_fields = ("name",)
    exclude = ["name", ]
