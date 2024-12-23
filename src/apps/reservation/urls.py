from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("", views.make_reservation, name="reserve"),
]
