from django.contrib import admin
from .models import CommonUser


@admin.register(CommonUser)
class CommonUserAdmin(admin.ModelAdmin):
    # items to be shown in users admin main list
    list_display = ["name", "adm_or_res"]
    search_fields = ("name",)
