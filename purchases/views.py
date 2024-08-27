from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import PurchaseToken


def simulate_purchase(request):
    token = get_random_string(length=32)
    expires_at = timezone.now() + timedelta(days=7)
    PurchaseToken.objects.create(token=token, expires_at=expires_at)

    return JsonResponse(
        {"token": token, "message": "Token has been successfully created."}
    )


def send_registration_email(user_email, token):
    # registration_url = "reverse()"
    pass
