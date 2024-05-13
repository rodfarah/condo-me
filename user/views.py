from django.shortcuts import render, redirect
from .forms import RegisterForm


def register_success(request):
    return render(request, "user/pages/success.html")


def register_view(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:success")
    else:
        form = RegisterForm()
    return render(request, "user/pages/register.html", {"form": form})
