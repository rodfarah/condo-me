from django.contrib.auth.models import AbstractUser, Group, Permission
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

    # Some conflicts happened with these two Django classes.
    # Need this changes bellow
    groups = models.ManyToManyField(
        to=Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(
        to=Permission,
        related_name="custom_user_permissions",
        blank=True
    )

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
        null=True,
        verbose_name="Leave this field blank if you do not want to \
            add more privileges than already set from its group"
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # If user is administrator, remove resident relations
        if self.adm_or_res == 'administrator':
            self.resident_condominium = None
            self.ResidentApartment.clear()
        # If user is resident, remove administrator relations
        else:
            self.administrator_condominium = None
        super().save(*args, **kwargs)
