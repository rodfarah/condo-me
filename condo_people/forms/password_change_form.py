from django.contrib.auth.forms import PasswordChangeForm

from condo_people.models import User


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(user, *args, **kwargs)
