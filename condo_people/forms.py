# there is this forms library
from django import forms
# there is this class that deals with password check and hash
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# we need to import User class in order to associate users with forms
from .models import User


# it is VERY IMPORTANT to use UserCreationForm because it deals with
# password check and hashing
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    # Meta sends metadata from my model to Django

    class Meta:
        model = User
        # which fields I want to use?
        fields = {
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        }

    def clean_email(self):
        email_in_form = self.cleaned_data.get('email')
        email_in_db = User.objects.filter(email__exact=email_in_form)
        if email_in_db.exists():
            raise ValidationError(
                'This e-mail address has been already used. Please, choose '
                'a different one.')
        return email_in_form

    def clean(self):
        """Check if both passwords are equal in register form"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error(field='password2',
                           error='The two passwords must match.')
        return cleaned_data
