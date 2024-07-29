from django import forms

from reservation.models import Reservation


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
