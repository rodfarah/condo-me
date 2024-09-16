from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "apartment",
        "display_groups",
    ]
    list_filter = ["groups"]

    fields = [
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "groups",
        "condominium",
        "apartment",
        "date_joined",
        "is_active",
        "last_login",
        "image",
    ]

    # customized method in order to show groups on list display
    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = "Groups"
