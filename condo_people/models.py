from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from condo.models import Apartment, Condominium


class User(AbstractUser):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, null=True,
        blank=True,
        related_name='residents')
    condominium = models.ForeignKey(
        Condominium, on_delete=models.CASCADE, null=True,
        blank=True,
        related_name='residents')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
