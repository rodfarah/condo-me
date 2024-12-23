from apps.purchase.models import RegistrationToken
from django.contrib import admin


@admin.register(RegistrationToken)
class RegistrationTokenAdmin(admin.ModelAdmin):
    list_display = [
        "register_email",
        "register_group",
        "token",
        "created_at",
        "expires_at",
        "not_used_yet",
    ]

    list_filter = ["register_group"]
