from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'common_area',
        'get_apartments',
        'date',
        'start_time',
        'end_time',
        'share_with_others',
        'active',
    ]
    readonly_fields = [
        "created_at",
        "updated_at"
    ]
