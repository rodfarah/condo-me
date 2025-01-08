from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.condo.models import Apartment, Condominium


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="first name", max_length=150, blank=False
    )
    last_name = models.CharField(verbose_name="last name", max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="condo_person",
    )
    condominium = models.ForeignKey(
        Condominium,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="condo_person",
    )
    cover = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        app_label = "condo_people"
