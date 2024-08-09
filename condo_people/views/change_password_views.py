from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "condo_people/registration/password_change.html"
    form_class = PasswordChangeForm

    @method_decorator(
        login_required(
            login_url="condo_people:login", redirect_field_name="redirect_to"
        )
    )
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        super().form_valid(form)
        messages.success(
            self.request,
            message="Your password has been successfully changed. Please, Log In.",
        )
        logout(self.request)
        return redirect("condo_people:login")

    def get_success_url(self) -> str:
        return reverse("condo_people:login")
