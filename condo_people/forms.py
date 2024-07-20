# there is this forms library
from django import forms
# there is this class that deals with password check and hash
from django.contrib.auth.forms import UserCreationForm

# we need to import User class in order to associate users with forms
from .models import User


# it is VERY IMPORTANT to use UserCreatioForm because it deals with
# password check and hashing
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    # Meta sends metadata from my model to Django

    class Meta:
        model = User
        # which fiels I want to use?
        fields = {
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        }
