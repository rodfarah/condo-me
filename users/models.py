from django.contrib.auth.models import AbstractUser
from django.db import models


class Manager(AbstractUser):
    # "name" field is not suposed to be shown on admin panel.
    # Abstract User only has "first_name" and "last_name"
    # be aware that "name" will be saved on "save" method down bellow
    name = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='condo_me/users/%Y/%m/%d/', blank=True)
    manager_condominium = models.ForeignKey(
        to='condo.Condominium',
        related_name='managers',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # AbstractUser does not have "name" field, so
        self.name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


class Caretaker(AbstractUser):
    # "name" field is not suposed to be shown on admin panel.
    # Abstract User only has "first_name" and "last_name"
    # be aware that "name" will be saved on "save" method down bellow
    name = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='condo_me/users/%Y/%m/%d/', blank=True)
    caretaker_condominium = models.ForeignKey(
        to='condo.Condominium',
        related_name='caretakers',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # AbstractUser does not have "name" field, so
        self.name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


class Resident(AbstractUser):
    # "name" field is not suposed to be shown on admin panel.
    # Abstract User only has "first_name" and "last_name"
    # be aware that "name" will be saved on "save" method down bellow
    name = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='condo_me/users/%Y/%m/%d/', blank=True)
    resident_condominium = models.ForeignKey(
        to='condo.Condominium',
        related_name='residents',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # AbstractUser does not have "name" field, so
        self.name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)
