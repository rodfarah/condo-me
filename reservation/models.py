from django.core.exceptions import ValidationError
from django.db import models

from condo.models import CommonArea, Condominium
from condo_people.models import User


class Reservation(models.Model):
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="reservations")
    common_area = models.ForeignKey(
        to=CommonArea, on_delete=models.CASCADE, related_name="reservations")
    user = models.ManyToManyField(to=User, related_name="reservations")
    date = models.DateField(
        verbose_name="Reservation Date", blank=False, null=False)
    start_time = models.TimeField(
        verbose_name="From:",
        blank=True,
        null=True,
        help_text="Leave blank if this is a whole day use common area"
    )
    end_time = models.TimeField(
        verbose_name="Until:",
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

    def get_apartments(self):
        users = self.user.all()
        return ", ".join(str(user.apartment) for user in users)

    get_apartments.short_description = "Apartments"
