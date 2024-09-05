from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone


class RegistrationToken(models.Model):
    customer_first_name = models.CharField(max_length=100, blank=False, null=True)
    customer_last_name = models.CharField(max_length=100, blank=False, null=True)
    customer_email = models.EmailField(max_length=200, blank=False, null=True)
    customer_group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    not_used_yet = models.BooleanField(default=True)

    def is_valid(self):
        expiration_validation = self.expires_at > timezone.now()
        return self.not_used_yet and expiration_validation

    def __str__(self):
        return f"Token created for {self.customer_group} {self.customer_email}"
