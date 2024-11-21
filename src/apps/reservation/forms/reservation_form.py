from apps.reservation.models import Reservation
from django import forms


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = {
            "user",
            "common_area",
            "date",
            "start_time",
            "end_time",
            "share_with_others",
        }
