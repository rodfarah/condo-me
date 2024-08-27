from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("simulate-purchase/", views.simulate_purchase, name="simulate_purchase"),
]
