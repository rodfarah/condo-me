from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    if "register_form_data" in request.session:
        del request.session["register_form_data"]
    return render(
        request,
        "condo_people/pages/register.html",
        context={
            "form": form,
        },
    )


def register_create(request):
    if request.method != "POST":
        raise Http404()

    form = RegisterForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "You are now registered, please log in.")
        request.session.pop("register_form_data", None)
        return redirect("condo_people:login")
    else:
        request.session["register_form_data"] = request.POST
        return redirect(to="condo_people:register")


def login_view(request):
    form = LoginForm()
    return render(request, "condo_people/pages/login.html", context={"form": form})


def login_create(request):
    if request.method != "POST":
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # returns an authenticated user object
        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect(reverse("condo:home"), {"user": authenticated_user})
        else:
            messages.error(
                request, "Invalid username and/or password. Please, try again."
            )
    else:
        return render(request, "condo_people/pages/login.html", context={"form": form})
    return redirect(reverse("condo_people:login"))
