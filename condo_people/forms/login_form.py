from django import forms
from django.contrib.auth.forms import UsernameField


class LoginForm(forms.Form):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        error_messages={"required": "Please, inform your username."},
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(),
        error_messages={"required": "You must inform your password"},
    )
