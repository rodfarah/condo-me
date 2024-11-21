from django import forms
from django.contrib.auth import forms as auth_forms


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label="type your e-mail",
        label_suffix="",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )


class CustomPasswordResetConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label="type your new password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="confirm your new password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )
