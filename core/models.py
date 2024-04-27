from django.db import models
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


class Condominium(models.Model):
    name = models.CharField(max_length=120)
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
    cover = models.ImageField(upload_to='condo_me/condominiums/%Y/%m/%d/')

    def __str__(self) -> str:
        return self.name

    def num_of_blocks(self):
        return self.block_set.count()

    def num_of_apartments(self):
        apartments_qty = 0
        for block in self.block_set.all():
            apartments_qty += block.num_of_apartments()
        return apartments_qty


class Block(models.Model):
    name = models.CharField(max_length=50)
    condominium = models.ForeignKey(to=Condominium, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def num_of_apartments(self):
        return self.apartment_set.count()


class Apartment(models.Model):
    number = models.IntegerField()
    block = models.ForeignKey(to=Block, on_delete=models.CASCADE)
    condominium = models.ForeignKey(to=Condominium, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Apt. {self.number}, Block: {self.block.name}"


class CommonArea(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
