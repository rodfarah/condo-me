from django.contrib import admin

from condo_people.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'apartment',
        'group'
    ]
    list_filter = ['groups']

    fields = [
        'first_name',
        'last_name',
        'username',
        'email',
        'password',
        'condominium',
        'apartment',
        'group',
        'date_joined',
        'is_active',
        'last_login',
        'image'
    ]
