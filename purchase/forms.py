from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import CreateManagerToken


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = CreateManagerToken

        fields = ["first_name", "last_name", "email"]

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
        }

        error_messages = {
            "first_name": {"required": "Please, insert a valid first name."},
            "last_name": {"required": "Please, insert a valid last name."},
            "email": {"required": "Please, insert a valid e-mail address."},
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                    "autocomplete": True,
                    "id": "firstName",
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": True,
                    "id": "lastName",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "autocomplete": True,
                    "id": "firstName",
                    "required": True,
                }
            ),
        }

    def clean_email(self):
        email_in_form = self.cleaned_data.get("email")
        email_in_user_db = get_user_model().objects.filter(email__iexact=email_in_form)
        email_in_token_db = CreateManagerToken.objects.filter(
            email__iexact=email_in_form
        )
        if email_in_user_db.exists():
            raise ValidationError(
                "This e-mail address has been already used. Please, choose "
                "a different one.",
                code="invalid",
            )
        elif email_in_token_db.exists():
            raise ValidationError(
                "You have already sent a registration link to your email "
                "address. Please, contact us for further information."
            )
        return email_in_form
