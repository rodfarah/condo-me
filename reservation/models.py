from django.db import models
from condo.models import CommonArea, Condominium, Apartment


class Reservation(models.Model):
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="reservations")
    common_area = models.ForeignKey(
        to=CommonArea, on_delete=models.CASCADE, related_name="reservations")
    apartments = models.ManyToManyField(
        to=Apartment, related_name="reservations", blank=True)
    # According to chatGPT, it is not necessary to create "apartments" or even
    # "users" here. Once both are many-to-many, Django creates it automaticaly.
    date = models.DateField(
        verbose_name="Reservation Date", blank=False, null=False)
    start_time = models.TimeField(
        verbose_name="User will start to use the common area at:",
        blank=False, null=False)
    end_time = models.TimeField(
        verbose_name="User will end to use the common area at:",
        blank=False, null=False)
    share_with_others = models.BooleanField(
        verbose_name="Main user may share common area with other users?")
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
