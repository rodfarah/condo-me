from django import forms
from django.core.exceptions import ValidationError
from django_countries import countries

from apps.condo.models import Apartment, Block, Condominium


class CondoSetupForm(forms.ModelForm):

    country = forms.ChoiceField(choices=countries)

    class Meta:
        model = Condominium

        fields = [
            "name",
            "description",
            "cnpj",
            "address1",
            "address2",
            "city",
            "state",
            "country",
            "postal_code",
            "cover",
        ]

        labels = {
            "name": "Condominium Name",
            "description": "Condominium Description",
            "cnpj": "CNPJ",
            "address1": "Street/Avenue Name, Number",
            "address2": "Neighbourhood",
            "city": "City Name",
            "state": "State",
            "country": "Country",
            "postal_code": "Zip Code",
            "cover": "Image",
        }

        error_messages = {
            "name": {"required": "Please, insert the condominium name."},
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": False,
                    "autocomplete": "on",
                    "id": "name",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "description",
                },
            ),
            "cnpj": forms.TextInput(
                attrs={
                    "placeholder": "XX.XXX.XXX/XXXX-XX",
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "cnpj",
                }
            ),
            "address1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "address1",
                }
            ),
            "address2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "address2",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "city",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "state",
                }
            ),
            "country": forms.Select(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "country",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "postal_code",
                }
            ),
            "cover": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "cover"}
            ),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj")

        self.instance.cnpj = cnpj
        try:
            # First, lets use the model validation
            self.instance.clean_cnpj()
        except ValidationError as e:
            raise forms.ValidationError(e.message)

        # Check if CNPJ already exists in db
        if Condominium.objects.filter(cnpj=cnpj).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "This CNPJ is already used. Please, consider choosing a different one."
            )
        return self.instance.cnpj


class BlockSetupForm(forms.ModelForm):

    apartments_count = forms.IntegerField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "id": "apartments_count"}
        ),
    )

    class Meta:
        model = Block

        fields = [
            "name",
            "description",
            "cover",
        ]

        labels = {
            "name": "Block Name",
            "description": "Description",
            "cover": "Image",
        }

        error_messages = {
            "name": {"required": "Please, insert the block name."},
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": False,
                    "autocomplete": "on",
                    "id": "name",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "description",
                },
            ),
            "cover": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "cover"}
            ),
        }

    def clean_name(self):
        block_name_in_form = self.cleaned_data.get("name")
        instance = self.instance  # Current instance beeing edited

        # Check if block name already exists in db, excluding instance
        if (
            Block.objects.filter(
                name=block_name_in_form,
            )
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "Block name already exists in this condominium. Please, choose a different one."
            )
        return block_name_in_form


class ApartmentSetupForm(forms.ModelForm):

    class Meta:
        model = Apartment

        fields = [
            "number_or_name",
        ]

        labels = {"number_or_name": "Apartment Number or Name"}

        error_messages = {
            "number_or_name": {
                "required": "Please, insert the apartment number or name."
            }
        }

        widgets = {
            "number_or_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                    "autocomplete": "on",
                    "id": "number_or_name",
                }
            ),
        }

    def clean_name(self):
        apartment_name_in_form = self.cleaned_data.get("number_or_name")
        instance = self.instance  # current instance beeing edited

        if (
            Apartment.objects.filter(
                number_or_name=apartment_name_in_form,
                condominium=instance.condominium,
                block=instance.block,
            )
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Apartment number (or name) already exists in this block. Please, choose a different one."
            )
        return apartment_name_in_form
