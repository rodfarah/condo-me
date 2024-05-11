from django.db import models
from condo.models import CommonArea, Condominium, Apartment
from django.core.exceptions import ValidationError


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
        blank=True,
        null=True,
        help_text="Leave blank if this is a whole day use common area"
    )
    end_time = models.TimeField(
        verbose_name="User will end to use the common area at:",
        blank=True,
        null=True,
        help_text="Leave blank if this is a whole day use common area"
    )
    share_with_others = models.BooleanField(
        verbose_name="Main user may share common area with other users?")
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.common_area.whole_day and (self.start_time or self.end_time):
            raise ValidationError(
                "No need to fill start and end fields. The common area you \
                    selected can only be reserved for the entire day of use.")
