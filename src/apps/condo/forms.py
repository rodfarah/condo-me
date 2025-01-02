from django import forms
from django.core.exceptions import ValidationError
from django_countries import countries

from apps.condo.models import Block, Condominium


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
            "cover": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "cover"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["apartments_count"].initial = (
                self.instance.get_apartments_count()
            )

    def clean_name(self):
        block_name_in_form = self.cleaned_data.get("name")
        instance = self.instance  # Current instance beeing edited

        # Check if block name already exists in db, excluding instance
        if (
            Block.objects.filter(name=block_name_in_form)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Block name already exists in this condominium. Please, choose a different one."
            )
        return block_name_in_form
