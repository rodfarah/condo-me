from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from condo.models import Apartment, Block, Condominium


class User(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Meta:
    db_table = 'condo_people_user'
    verbose_name = 'User'
    verbose_name_plural = 'Users'


class Resident(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='resident_profile')
    condominium = models.ForeignKey(
        Condominium, on_delete=models.CASCADE,
        related_name='resident_condominium')
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='resident_apartment'
    )
    block = models.ForeignKey(
        Block,
        on_delete=models.CASCADE,
        related_name='resident_block'
    )
    image = models.ImageField(
        upload_to='condo_me/users/%Y/%m/%d/', blank=True)


class CondoManager(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='condmanager_profile'
    )
    condominium = models.ForeignKey(
        Condominium, on_delete=models.CASCADE,
        related_name='condmanager_condominium')
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='condmanager_apartment',
        blank=True,
    )
    block = models.ForeignKey(
        Block,
        on_delete=models.CASCADE,
        related_name='condmanager_block',
        blank=True,
    )
    image = models.ImageField(
        upload_to='condo_me/users/%Y/%m/%d/', blank=True)


class CareTaker(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='caretaker_profile'
    )
    condominium = models.ForeignKey(
        Condominium,
        on_delete=models.CASCADE,
        related_name='caretaker_condominium'
    )
    image = models.ImageField(
        upload_to='condo_me/users/%Y/%m/%d/', blank=True)
    lives_in_condo = models.BooleanField()


# Had to code bellow despite of an Reverse accessor error on migrate.
Group._meta.get_field('user_set').related_name = 'auth_groups'
Permission._meta.get_field('user_set').related_name = 'auth_permissions'
