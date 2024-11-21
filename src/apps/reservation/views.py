from django.shortcuts import render

from .forms.reservation_form import ReservationForm


def make_reservation(request):
    form = ReservationForm()
    return render(
        request=request,
        template_name="reservation/pages/reservation.html",
        context={"form": form},
    )
