from django import forms
from django.core.exceptions import ValidationError
from django_countries import countries

from apps.condo.models import Apartment, Block, CommonArea, Condominium


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
        required=True,
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
        required=True,
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
        required=True,
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

    def clean_last_floor(self):
        last_floor_in_form = self.cleaned_data.get("last_floor")

        if last_floor_in_form is None or last_floor_in_form < self.cleaned_data.get(
            "first_floor"
        ):
            raise ValidationError(
                "Last floor number must be equal or higher than first floor number"
            )
        return last_floor_in_form


class CommonAreaSetupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # maximum using time is automatically calculated on models and must be a read
        # only field in form
        if "maximum_using_time" in self.fields:
            self.fields["maximum_using_time"].widget.attrs["readonly"] = True

    class Meta:
        model = CommonArea

        fields = [
            "name",
            "description",
            "opens_at",
            "closes_at",
            "whole_day",
            "paid_area",
            "price",
            "minimum_using_minutes",
            "maximum_using_fraction",
            "maximum_using_time",
            "cover",
        ]

        labels = {
            "name": "Common Area Name",
            "description": "Description",
            "opens_at": "Opening time",
            "closes_at": "Closing time",
            "whole_day": "Whole day reservation?",
            "paid_area": "Residents must pay in order to use this common area?",
            "price": "Please, enter the price per use:",
            "minimum_using_minutes": "Minimum usage time (in minutes) for a reservation:",
            "maximum_using_fraction": "Maximum using fraction:",
            "maximum_using_time": "Maximum number of minutes a user may use this common area per day",
            "cover": "Common area image",
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
            "opens_at": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "opens_at",
                    "type": "time",
                    "step": "60",
                },
                format="%H:%M",
            ),
            "closes_at": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "closes_at",
                    "type": "time",
                    "step": "60",
                },
                format="%H:%M",
            ),
            "whole_day": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "autocomplete": "on",
                    "id": "whole_day",
                    "data-toggle": "tooltip",
                    "title": "Click if resident may use the common area for the entire day with only one reservation",
                    "aria-describedby": "wholeDayHelp",
                },
            ),
            "paid_area": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "autocomplete": "on",
                    "id": "paid_area",
                    "data-toggle": "tooltip",
                    "title": "Click this checkbox if this common area is pay-per-use.",
                    "aria-describedby": "paidAreaHelp",
                },
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "price",
                    "min": "0.01",
                    "step": "0.01",
                    "data-toggle": "tooltip",
                    "title": "Decimals are separated by '.'",
                },
            ),
            "minimum_using_minutes": forms.Select(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "minimum_using_minutes",
                    "data-toggle": "tooltip",
                    "title": "Choose a value from the list",
                    "aria-describedby": "minimumUsingMinutesHelp",
                },
            ),
            "maximum_using_fraction": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "maximum_using_fraction",
                    "min": "1",
                    "data-toggle": "tooltip",
                    "title": "Enter a positive integer",
                    "aria-describedby": "maximumUsingFractionHelp",
                },
            ),
            "maximum_using_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": "on",
                    "id": "maximum_using_time",
                },
            ),
            "cover": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "cover"}
            ),
        }

    def clean_closes_at(self):
        closing_time_in_form = self.cleaned_data.get("closes_at")
        oppening_time_in_form = self.cleaned_data.get("opens_at")

        if (
            oppening_time_in_form
            and closing_time_in_form
            and closing_time_in_form <= oppening_time_in_form
        ):
            raise ValidationError("Closing time must be higher than opening time.")
        return closing_time_in_form
