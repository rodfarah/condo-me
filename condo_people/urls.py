from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .forms.password_reset_forms import CustomPasswordResetForm

app_name = "condo_people"

urlpatterns = [
    # REGISTER
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    # LOGIN
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    # LOGOUT
    path("logout/", views.logout_view, name="logout"),
    # PASSWORD CHANGE
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    # PASSWORD RESET
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="condo_people/registration/password_reset.html",
            email_template_name="condo_people/registration/password_reset_email.html",
            success_url=reverse_lazy(
                "condo_people:password_reset_done",
            ),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="condo_people/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="condo_people/registration/password_reset_confirm.html",
            success_url="/condo_people/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="condo_people/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
