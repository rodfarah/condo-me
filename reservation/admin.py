from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = [
        "created_at",
        "updated_at"
    ]
