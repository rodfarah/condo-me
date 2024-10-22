# there is this forms library
from django import forms

# Instead of declaring which User model to use in the form,
# it is highly reccomended to use get_user_model function
from django.contrib.auth import get_user_model

# there is this class that deals with password check and hash
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


# it is VERY IMPORTANT to use UserCreationForm because it deals with
# password check, hashing and other validations
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = get_user_model()
        # which fields I want to use?
        fields = {
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        }

    def clean_email(self):
        email_in_form = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email_in_form).exists():
            raise ValidationError(
                "This e-mail address has been already used. Please, choose "
                "a different one."
            )
        return email_in_form

    # UserCreationForm already check if both passwords match!
