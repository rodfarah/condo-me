from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # autocomplete_fields = ["apartments", "users",]
    # fields = [
    #     "condominium",
    #     "common_area",
    #     "date",
    #     "start_time",
    #     "end_time",
    #     "share_with_others",
    #     "active",
    #     "created_at",
    #     "updated_at"
    # ]
    readonly_fields = [
        "created_at",
        "updated_at"
    ]
