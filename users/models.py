from django.contrib.auth.models import AbstractUser
from django.db import models


class CommonUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('administrator', 'Administrator'),
        ('resident', 'Resident')
    ]

    adm_or_res = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='condo_me/users/%Y/%m/%d/')

    administrator_condominium = models.ForeignKey(
        to='condo.Condominium',
        related_name='administrators',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    resident_condominium = models.ForeignKey(
        to='condo.Condominium',
        related_name='residents',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # If user is administrator, remove resident relations
        if self.adm_or_res == 'administrator':
            self.resident_condominium = None
            self.apartments.clear()
        # If user is resident, remove administrator relations
        else:
            self.administrator_condominium = None
        super().save(*args, **kwargs)
