from django.urls import path

from . import views

app_name = "condo_people"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_view, name="logout"),
    # password change
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    # path(
    #     "password-change/done/",
    #     views.CustomPasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
]
