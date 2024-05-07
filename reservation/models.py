from django.db import models
from condo.models import CommonArea, Condominium


class Reservation(models.Model):
    common_area = models.ForeignKey(
        to=CommonArea, on_delete=models.CASCADE, related_name="reservations")
    # According to chatGPT, it is not necessary to create "apartments" or even
    # "users" here. Once both are many-to-many, Django creates it automaticaly.
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
