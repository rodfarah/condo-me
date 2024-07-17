from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
    'common_area',
    'date',
    # 'apartments',
    'active',
    ]
    readonly_fields = [
        "created_at",
        "updated_at"
    ]
