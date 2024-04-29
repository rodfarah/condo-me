from django.contrib.auth.models import AbstractUser
from django.db import models
from condo.models import Condominium


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('resident', 'Resident'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    condominium = models.ForeignKey(to=Condominium, on_delete=models.CASCADE)
