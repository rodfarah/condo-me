from apps.condo.models import Apartment, Condominium
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="first name", max_length=150, blank=False
    )
    last_name = models.CharField(verbose_name="last name", max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="residents",
    )
    condominium = models.ForeignKey(
        Condominium,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="residents",
    )
    cover = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
