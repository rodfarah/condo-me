from datetime import timedelta

from apps.purchase.models import RegistrationToken
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from .forms import PurchaseForm


def purchase_view(request):
    form = PurchaseForm()
    return render(request, "purchase/pages/purchase.html", context={"form": form})


def purchase_create(request):
    # Set days to expire
    DAYS_TO_EXPIRE = 30

    if request.method != "POST":
        raise Http404()

    form = PurchaseForm(data=request.POST)

    if form.is_valid():
        register_first_name = form.cleaned_data["register_first_name"]
        register_last_name = form.cleaned_data["register_last_name"]
        register_email = form.cleaned_data["register_email"]
        register_group = Group.objects.get(name__iexact="manager")
        # Set up a new token.
        crypted_token = get_random_string(length=32)
        expires_at = timezone.now() + timedelta(days=DAYS_TO_EXPIRE)
        # Create a token object in db.
        RegistrationToken.objects.create(
            register_first_name=register_first_name,
            register_last_name=register_last_name,
            register_email=register_email,
            register_group=register_group,
            token=crypted_token,
            expires_at=expires_at,
        )
        registration_link = request.build_absolute_uri(
            reverse("condo_people:register", args=[crypted_token])
        )
        send_mail(
            subject="Your registration link",
            message=f"Please, click on the following link to complete your Condo_Me registration: {registration_link}",
            from_email="no-reply@condome.com",
            # Have to colect from a form
            recipient_list=[register_email],
            fail_silently=False,
        )
        return redirect(reverse("purchase:email_order"))
    return render(request, "purchase/pages/purchase.html", context={"form": form})


def check_email(request):
    return render(request, "purchase/pages/confirm_email.html")
