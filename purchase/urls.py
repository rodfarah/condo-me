from django.urls import path

from . import views

app_name = "purchase"

urlpatterns = [
    path("order/", views.purchase_view, name="purchase_order"),
    path("create/", views.purchase_create, name="purchase_create"),
    path("check-your-email/", views.check_email, name="email_order"),
]
