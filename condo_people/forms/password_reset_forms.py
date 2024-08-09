from django import forms
from django.contrib.auth import forms as auth_forms


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control rounded-3",
                "placeholder": "your e-mail address",
                "id": "floatingUserName",
            }
        ),
    )
