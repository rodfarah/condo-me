from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.purchase.models import RegistrationToken

from .forms import LoginForm, RegisterForm


def register_view(request, token):
    # Check if Token exists
    try:
        token_obj = RegistrationToken.objects.get(token=token)
        if not token_obj.is_valid():
            return redirect(reverse("condo_people:invalid_token"))
    except RegistrationToken.DoesNotExist:
        # Remove sessions from cookies if token does not exist or invalid.
        request.session.pop("register_form_data", None)
        request.session.pop("token", None)
        # Redirect user to invalid token template
        return redirect(reverse("condo_people:invalid_token"))
    else:
        # If there is no session, variable equals None ...
        register_form_data = request.session.get("register_form_data", None)
        # ...and form will be empty
        form = RegisterForm(register_form_data)
        # Clear form data session
        request.session.pop("register_form_data", None)
        # Store token in session for later use.
        request.session["token"] = token
        return render(
            request,
            "condo_people/registration/register.html",
            context={
                "form": form,
            },
        )


def register_create(request):
    if request.method != "POST":
        raise Http404()

    form = RegisterForm(request.POST)

    if form.is_valid():
        # For security reasons, manually set password in order to hash it
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password1"])
        new_user.save()

        # Assign token as 'used'
        token = request.session["token"]
        token = RegistrationToken.objects.get(token__iexact=token)
        token.not_used_yet = False
        token.save()

        # set user to corresponding group (manager, caretaker or resident)
        new_user_group = token.register_group
        new_user.groups.add(new_user_group)

        request.session.flush()
        # Redirect user to login page.
        messages.success(request, "You are now registered, please log in.")
        return redirect(reverse("condo_people:login"))
    else:
        request.session["register_form_data"] = request.POST
        return redirect(
            reverse(
                "condo_people:register",
                kwargs={"token": request.session.get("token")},
            )
        )


def invalid_token(request):
    return render(request, "condo_people/registration/invalid_token.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("condo:home"))
    form = LoginForm()
    return render(
        request, "condo_people/registration/login.html", context={"form": form}
    )


def login_create(request):
    if request.method != "POST":
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user_model = get_user_model()
        # Check if user exists in db in order to differenciate "is_active" users.
        # consider Django does not authenticate inactive users. So we have to authenticate
        # later on.
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user = None

        if user is not None:
            # If user is not active
            if not user.is_active:
                messages.error(request, "Disabled Account")
                return redirect(reverse("condo_people:login"))
            # may return an authenticated user object (if username and pwd are correct)
            authenticated_user = authenticate(
                request, username=username, password=password
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect(reverse("condo:home"), {"user": authenticated_user})
        # user is None
        messages.error(request, "Invalid username and/or password. Please, try again.")
        return redirect(reverse("condo_people:login"))
    # if form is not valid
    return render(request, "condo_people/registration/login.html", {"form": form})


# login_url: to send user in case user is not logged in
# redirect_field_name: /login/?redirect_to=/logout_view/ means that after log in,
# django will send user to "logout_view".
# @login_required(login_url="condo_people:login", redirect_field_name="redirect_to")
@login_required(login_url="condo_people:login", redirect_field_name="redirect_to")
def logout_view(request):
    # Ensure the logout is only done via POST
    if request.method == "POST":
        logout(request)
    return redirect(reverse("condo_people:login"))


class CustomPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    success_message = "Your password has been changed successfully."
