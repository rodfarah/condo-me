from django.contrib.auth import get_user_model
from django.test import TestCase


class CondoPeopleTestBase(TestCase):
    def create_test_user(
        self,
        first_name="Elliot",
        last_name="Smith",
        email="elliot@smith.com",
        username="elliotsmith",
        password="BetweenTheBars",
        is_active=True,
    ):

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            is_active=is_active,
        )
        return self.user

    def login_test_user(self):
        return self.client.login(username="elliotsmith", password="BetweenTheBars")
