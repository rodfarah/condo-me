from datetime import timedelta

from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from .forms import PurchaseForm
from .models import CreateManagerToken


def purchase_view(request):
    form = PurchaseForm()
    return render(request, "purchase/pages/purchase.html", context={"form": form})


def purchase_create(request):
    if request.method != "POST":
        raise Http404()

    form = PurchaseForm(data=request.POST)

    if form.is_valid():
        customer_email = form.cleaned_data["email"]
        customer_first_name = form.cleaned_data["first_name"]
        customer_last_name = form.cleaned_data["last_name"]
        customer_group = Group.objects.get(name__iexact="manager")
        # Create a new token.
        crypted_token = get_random_string(length=32)
        expires_at = timezone.now() + timedelta(days=7)
        CreateManagerToken.objects.create(
            first_name=customer_first_name,
            last_name=customer_last_name,
            email=customer_email,
            group=customer_group,
            token=crypted_token,
            expires_at=expires_at,
        )
        registration_link = request.build_absolute_uri(
            reverse("purchase:purchase_order", args=[crypted_token])
        )
        send_mail(
            subject="Your registration link",
            message=f"Please, click on the following link to complete your Condo_Me registration: {registration_link}",
            from_email="no-reply@condome.com",
            # Have to colect from a form
            recipient_list=[customer_email],
            fail_silently=False,
        )

        return JsonResponse(
            {"message": "Token has been successfully created and sent via e-mail"}
        )
    return render(request, "purchase/pages/purchase.html", context={"form": form})


def check_email(request):
    return render(request, "purchase/pages/confirm_email.html")
