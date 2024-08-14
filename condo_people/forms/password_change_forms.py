from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="current password",
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "old password",
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )

    new_password1 = forms.CharField(
        label="new password",
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="confirm new password",
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-3",
                "placeholder": "",
            }
        ),
    )
