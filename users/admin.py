from django.contrib import admin
from .models import CommonUser


@admin.register(CommonUser)
class CommonUserAdmin(admin.ModelAdmin):
    pass
