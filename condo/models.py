from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


class Condominium(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    cnpj = models.CharField(
        max_length=18,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$',
                message='CNPJ number mask must be XX.XXX.XXX/XXXX-XX')],
        unique=True)
    street = models.CharField(max_length=150)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=100, blank=True, null=True)
    neighborwood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    country = CountryField()
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='condo_me/condominiums/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return self.name

    def num_of_blocks(self):
        return self.blocks.count()

    def num_of_apartments(self):
        apartments_qty = 0
        for block in self.blocks.all():
            apartments_qty += block.num_of_apartments()
        return apartments_qty


class Block(models.Model):
    name = models.CharField(max_length=50, default="Main Block")
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="blocks",
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def num_of_apartments(self):
        return self.apartments.count()


class Apartment(models.Model):
    number_or_name = models.CharField(
        max_length=20, verbose_name="Number (or name)")
    block = models.ForeignKey(
        to=Block, on_delete=models.CASCADE, related_name="apartments")
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="apartments")
    residents = models.ManyToManyField(
        to="user.User", related_name="apartments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number_or_name', 'block']

    def __str__(self) -> str:
        return self.number_or_name

    def num_of_residents(self):
        return self.residents.count()


class CommonArea(models.Model):

    MINIMUM_USING_MINUTES = [
        (30, '30'),
        (60, '60')
    ]

    name = models.CharField(max_length=50)
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="common_areas")
    opens_at = models.TimeField(auto_now=False, blank=False)
    closes_at = models.TimeField(auto_now=False, blank=False)
    whole_day = models.BooleanField(
        verbose_name="Must be a whole day reservation?")
    paid_area = models.BooleanField(verbose_name="User have to pay for use?")
    price = models.DecimalField(
        "Price", max_digits=5, decimal_places=2, blank=True, null=True)
    minimum_using_minutes = models.IntegerField(
        "Minimum using time in minutes",
        choices=MINIMUM_USING_MINUTES,
        blank=True, null=True)
    maximum_using_fraction = models.IntegerField(
        verbose_name="Choose an integer. It will be multiplied by minimum \
            using minutes (above) in order to obtain maximum using time \
                (bellow)",
        blank=True,
        null=True)
    # this field will be automaticaly calculated on __init__
    maximum_using_time = models.IntegerField(
        blank=True, null=True, verbose_name="Maximum using time (minutes)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='condo_me/common_areas/%Y/%m/%d/', blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def calc_maximum_usage(self):
        if self.minimum_using_minutes and self.maximum_using_fraction:
            return self.minimum_using_minutes * self.maximum_using_fraction

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.maximum_using_time = self.calc_maximum_usage()

    def clean(self):
        if self.whole_day and self.maximum_using_time:
            raise ValidationError(
                "No need to choose maximum minutes of use per day in case \
                    of whole day reservation")
        elif self.paid_area and not self.price:
            raise ValidationError(
                "You confirmed this is a paid common area.Please inform usage \
                    price.")
        elif not self.paid_area and self.price:
            raise ValidationError(
                "You confirmed this is NOT a paid common area. Please remove \
                    its usage price.")
        elif self.whole_day and (
            self.minimum_using_minutes or self.maximum_using_fraction
        ):
            raise ValidationError(
                "If whole day reservation is selected, maximum minutes of \
                    use and/or maximum using fraction should not be \
                        specified.")
