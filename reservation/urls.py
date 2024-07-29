from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("reservation/", views.make_reservation, name="reserve"),
]
