from django import forms
from django.core.exceptions import ValidationError
from django_countries import countries

from .models import Condominium, Block


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
                    "id": "firstName",
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

    def clean_name(self):
        condo_name_in_form = self.cleaned_data.get("name")
        instance = self.instance  # Current instance beeing edited

        # Check if condo name already exists in db, excluding instance
        if (
            Condominium.objects.filter(name=condo_name_in_form)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Condominium name already exists. Please, choose a different one."
            )
        return condo_name_in_form

    # def clean_cnpj(self):
    #     condo_cnpj_in_form = self.cleaned_data.get("cnpj")

    #     # Check if CNPJ already exists in db
    #     if Condominium.objects.filter(cnpj=condo_cnpj_in_form).exists():
    #         raise ValidationError(
    #             "This CNPJ already exists. Please, choose a different one."
    #         )
    #     return condo_cnpj_in_form

class BlockSetupForm(forms.ModelForm):

    class Meta:
        model = Block

        fields = [
            "name",
            "description",
        ]

        labels = {
            "name": "Block Name",
            "description": "Description",
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
                    "id": "firstName",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "description",
                },
            ),
        }

    def clean_name(self):
        block_name_in_form = self.cleaned_data.get("name")
        instance = self.instance  # Current instance beeing edited

        # Check if condo name already exists in db, excluding instance
        if (
            Condominium.blocks.objects.filter(name=block_name_in_form)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Block name already exists in this condominium. Please, choose a different one."
            )
        return block_name_in_form