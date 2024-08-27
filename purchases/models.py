from django.db import models
from django.utils import timezone


class PurchaseToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    not_used_yet = models.BooleanField(default=True)

    def is_valid(self):
        expiration_validation = self.expires_at > timezone.now()
        return self.not_used_yet and expiration_validation
