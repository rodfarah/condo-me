from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from condo.models import Apartment, Condominium


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
    image = models.ImageField(upload_to="condo_me/condominiums/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# class ManagerRegistationLink(models.Model):
#     user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
#     code = models.CharField(max_length=64, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     used = models.BooleanField(default=False)
