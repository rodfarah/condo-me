from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from condo.models import Condominium
from reservation.models import Reservation


class User(AbstractUser):
    # There is this conflict related name between Group, Permission and User.
    # We need to change the related name here.
    groups = models.ManyToManyField(to=Group, related_name="users_groups")
    user_permissions = models.ManyToManyField(
        to=Permission, related_name="users_permissions")
    ROLES = [
        ("MANAGER", 'Manager'),
        ("Caretaker", "Caretaker"),
        ("RESIDENT", 'Resident'),
    ]
    user_role = models.CharField(max_length=10, choices=ROLES)

    condominium = models.ForeignKey(
        to=Condominium,
        related_name="users",
        on_delete=models.CASCADE
    )

    reservations = models.ManyToManyField(
        to=Reservation, related_name="users", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='condo_me/users/%Y/%m/%d/', blank=True)

    # "name" field is not suposed to be shown on admin panel.
    # Abstract User only has "first_name" and "last_name"
    # be aware that "name" will be saved on "save" method down bellow
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # AbstractUser does not have "name" field, so let's create one
        self.name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)
