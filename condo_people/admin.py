from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "apartment"]
    list_filter = ["groups"]

    fields = [
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "condominium",
        "apartment",
        "date_joined",
        "is_active",
        "last_login",
        "image",
    ]
