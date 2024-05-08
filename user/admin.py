from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    # list_display = ["name", "groups"]
    search_fields = ("name",)
    readonly_fields = [
        "created_at",
        "updated_at",
        "apartments",
        "reservations"
    ]
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        "groups",
        "is_active",
        "date_joined",
        "last_login",
        "image"
    ]
