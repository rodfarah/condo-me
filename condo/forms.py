from django import forms
from django.core.exceptions import ValidationError

from .models import Condominium


class CondoSetupForm(forms.ModelForm):
    class Meta:
        model = Condominium

        fields = [
            "name",
            "cnpj",
            "address1",
            "address2",
            "city",
            "state",
            "country",
            "postal_code",
            "description",
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
            "cnpj": {"required": "Please, insert a valid CNPJ number."},
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
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
            "country": forms.TextInput(
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
        # Check if condo name already exists in db
        if Condominium.objects.filter(name=condo_name_in_form).exists():
            raise ValidationError(
                "Condominium name already exists. Please, choose a different one."
            )
        return condo_name_in_form

    def clean_cnpj(self):
        condo_cnpj_in_form = self.cleaned_data.get("cnpj")

        # Check if CNPJ already exists in db
        if Condominium.objects.filter(cnpj=condo_cnpj_in_form).exists():
            raise ValidationError(
                "This CNPJ already exists. Please, choose a different one."
            )
        return condo_cnpj_in_form
