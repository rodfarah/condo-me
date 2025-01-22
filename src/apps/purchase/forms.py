from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.purchase.models import RegistrationToken


class PurchaseForm(forms.ModelForm):

    register_email2 = forms.EmailField(
        max_length=200,
        required=True,
        label="Confirm your e-mail",
        error_messages={"required": "Please, insert a valid e-mail address."},
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": True,
                "id": "email2",
                "required": True,
            }
        ),
    )

    class Meta:
        model = RegistrationToken

        fields = [
            "register_first_name",
            "register_last_name",
            "register_email",
            "register_email2",
        ]

        labels = {
            "register_first_name": "First Name",
            "register_last_name": "Last Name",
            "register_email": "E-mail",
        }

        error_messages = {
            "register_first_name": {"required": "Please, insert a valid first name."},
            "register_last_name": {"required": "Please, insert a valid last name."},
            "register_email": {"required": "Please, insert a valid e-mail address."},
        }

        widgets = {
            "register_first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                    "autocomplete": True,
                    "id": "name",
                    "required": True,
                }
            ),
            "register_last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": True,
                    "id": "lastName",
                    "required": True,
                }
            ),
            "register_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": True,
                    "id": "email1",
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        register_email_in_form = self.cleaned_data.get("register_email")
        register_email2_in_form = self.cleaned_data.get("register_email2")
        # Check if form registration e-mail addresses are the same.
        if register_email_in_form and register_email2_in_form:
            if register_email_in_form != register_email2_in_form:
                self.add_error(
                    "register_email2",
                    ValidationError(
                        "E-mail addresses don't match. Please, make sure both are the same.",
                        code="invalid",
                    ),
                )
        return cleaned_data

    def clean_register_email(self):
        register_email_in_form = self.cleaned_data.get("register_email")

        # Check if form registration e-mail is used by other User
        if (
            get_user_model()
            .objects.filter(email__iexact=register_email_in_form)
            .exists()
        ):
            raise ValidationError(
                "This e-mail address has been already used by other user. Please, choose "
                "a different one.",
                code="invalid",
            )
        return register_email_in_form
