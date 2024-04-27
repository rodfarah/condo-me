from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Condominium, Apartment


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('resident', 'Resident'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    condominium = models.ForeignKey(to=Condominium, on_delete=models.CASCADE)
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
