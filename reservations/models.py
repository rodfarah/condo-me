from django.db import models
from condo.models import Apartment, CommonArea, Condominium
from users.models import CommonUser


class Reservation(models.Model):
    owner = models.ForeignKey(
        to=CommonUser, on_delete=models.CASCADE, related_name="reservations")
    apartment = models.ForeignKey(
        to=Apartment, on_delete=models.CASCADE, related_name="reservations")
    common_area = models.ForeignKey(
        to=CommonArea, on_delete=models.CASCADE, related_name="reservations")
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="reservations")
    date = models.DateField(
        verbose_name="Reservation Date", blank=False, null=False)
    start_time = models.TimeField(
        verbose_name="Time user will start to use the common area",
        blank=False, null=False)
    end_time = models.TimeField(
        verbose_name="Time user will end to use the common area",
        blank=False, null=False)
    share_with_others = models.BooleanField(
        verbose_name="Main user may share common area with other users?")
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
