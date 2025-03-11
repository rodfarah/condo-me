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
                    "placeholder": "XX.XXX.XXX/XXXX-XX    or    ONLY NUMBERS",
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
            "number_or_name",
            "description",
            "cover",
        ]

        labels = {
            "number_or_name": "Block Name",
            "description": "Description",
            "cover": "Image",
        }

        error_messages = {
            "number_or_name": {
                "required": "Please, insert the block number (or_name)."
            },
        }

        widgets = {
            "number_or_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": False,
                    "autocomplete": "on",
                    "id": "number_or_name",
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


class ApartmentSetupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """A block must not have two apartments with identical number_or_name (see clean
         method bellow), so we must receive the "condominium" and "block" objects from
          the view once we can not access them from form fields.
        Notice that SetupApartmentCreateView() sends "condominium" and "block" through
        "get_form_kwargs()".
        """
        condominium = kwargs.pop("condominium", None)
        self.condominium = condominium
        block = kwargs.pop("block", None)
        self.block = block
        super().__init__(*args, **kwargs)

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

    def clean_number_or_name(self):
        apartment_number_or_name_in_form = self.cleaned_data.get("number_or_name")

        if (
            Apartment.objects.filter(
                number_or_name=apartment_number_or_name_in_form,
                condominium=self.condominium,
                block=self.block,
            )
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Apartment number (or name) already exists in this block. Please, choose a different one."
            )
        return apartment_number_or_name_in_form


class ApartmentMultipleSetupForm(forms.Form):

    first_floor = forms.IntegerField(
        label="Insert first floor number",
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "autocomplete": "on",
                "id": "first_floor",
            }
        ),
        error_messages={"required": "Please, insert first floor number."},
    )

    last_floor = forms.IntegerField(
        label="Insert last floor number",
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "autofocus": False,
                "autocomplete": "on",
                "id": "last_floor",
            }
        ),
        error_messages={"required": "Please, insert last floor number."},
    )

    apartments_per_floor = forms.IntegerField(
        label="Insert number of apartments per floor",
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "autofocus": False,
                "autocomplete": "on",
                "id": "apartments_per_floor",
            }
        ),
        error_messages={"required": "Please, insert number of apartments per floor."},
    )

    def __init__(self, *args, **kwargs) -> None:
        """A block must not have two apartments with identical number_or_name (see clean
            method bellow), so we must receive the "condominium" and "block" objects from
            the view once we can not access them from form fields.
        Notice that SetupApartmentCreateView() sends "condominium" and "block" through
        "get_form_kwargs()".
        """
        condominium = kwargs.pop("current_condominium", None)
        self.condominium = condominium
        block = kwargs.pop("current_block", None)
        self.block = block
        super().__init__(*args, **kwargs)

    def clean_first_floor(self):
        first_floor_in_form = self.cleaned_data.get("first_floor")

        if first_floor_in_form is None or first_floor_in_form < 0:
            raise ValidationError("First floor must be equal or higher than 0 (zero)")
        return first_floor_in_form

    def clean_last_floor(self):
        last_floor_in_form = self.cleaned_data.get("last_floor")

        if last_floor_in_form is None or last_floor_in_form < self.cleaned_data.get(
            "first_floor"
        ):
            raise ValidationError(
                "Last floor number must be equal or higher than first floor number"
            )
        return last_floor_in_form

    def clean_apartments_per_floor(self):
        apartments_per_floor_in_form = self.cleaned_data.get("apartments_per_floor")

        if apartments_per_floor_in_form is None or apartments_per_floor_in_form < 1:
            raise ValidationError("You must have at least one apartment per floor.")
        return apartments_per_floor_in_form
