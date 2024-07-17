from django.shortcuts import render, redirect
from .forms import RegisterForm


def register_success(request):
    return render(request, "users/pages/success.html")


def register_view(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:success")
        # else:
        #     return render(request, "users/pages/register.html", {"form": form, "errors": })
    else:
        form = RegisterForm()
    return render(request, "users/pages/register.html", {"form": form})

def login_view(request):
    pass