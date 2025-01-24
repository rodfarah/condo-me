from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.purchase.models import RegistrationToken


@pytest.mark.django_db
class TokenTestBase(TestCase):
    def setUp(self):
        # Make sure "manager" group is available
        self.manager_group, created = Group.objects.get_or_create(name="manager")

    def create_test_token(
        self,
        register_first_name="John",
        register_last_name="Doe",
        register_email="john@doe.com",
        token=get_random_string(length=32),
        expires_at=timezone.now() + timedelta(30),
    ):
        self.registration_token = RegistrationToken.objects.create(
            register_first_name=register_first_name,
            register_last_name=register_last_name,
            register_email=register_email,
            register_group=self.manager_group,
            token=token,
            expires_at=expires_at,
        )
        return self.registration_token


@pytest.mark.django_db
class CondoPeopleTestBase(TestCase):
    """
    Base test case for the Condo People application.
    This class provides utility methods for creating and logging in a test user.
    Methods:
        create_test_user(first_name, last_name, email, username, password, is_active):
            Creates and returns a test user with the specified attributes.
        login_test_user():
            Logs in the test user with predefined credentials.
    """

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
