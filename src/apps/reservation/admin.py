from apps.reservation.models import Reservation
from django.contrib import admin


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "common_area",
        "get_apartments",
        "date",
        "start_time",
        "end_time",
        "share_with_others",
        "active",
    ]
    readonly_fields = ["created_at", "updated_at"]
