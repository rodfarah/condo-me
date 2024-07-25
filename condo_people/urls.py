from django.urls import path

from . import views

app_name = "condo_people"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="create"),
    path("login/", views.login, name="login"),
]
