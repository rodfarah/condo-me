from django.shortcuts import redirect, render


def register_success(request):
    return render(request, "condo_people/pages/success.html")


def register_view(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("condo_people:success")
    else:
        form = RegisterForm()
    return render(request, "condo_people/pages/register.html", {"form": form})


def login_view(request):
    if request.POST:
        pass
