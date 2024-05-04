from django.contrib import admin
from .models import CommonUser


@admin.register(CommonUser)
class CommonUserAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    # list_display = ["name", "groups"]
    search_fields = ("name",)
    readonly_fields = [
        "created_at",
        "updated_at",
        "ResidentApartment",
        "reservations"
    ]
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        "groups",
        "resident_condominium",
        "is_active",
        "date_joined",
        "last_login",
        "image"
    ]
