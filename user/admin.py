from django.contrib import admin
from .models import RealUser


@admin.register(RealUser)
class UserAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    # list_display = ["name", "groups"]
    search_fields = ("name",)
    readonly_fields = [
        "created_at",
        "updated_at",
        "ResidentApartment",
        "reservation"
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
