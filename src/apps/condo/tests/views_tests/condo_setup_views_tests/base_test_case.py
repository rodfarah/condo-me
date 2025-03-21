from apps.condo.models import Condominium
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase


class BaseTestCase(TestCase):
    """This class has all commmon setup for all tests"""

    def setUp(self) -> None:
        """
        Set up the test environment for the condo setup views tests.
        This method performs the following actions:
        1. Calls the parent class's setUp method.
        2. Creates a user with the specified details.
        3. Creates a condominium with the specified details.
        4. Assigns the created condominium to the created user.
        5. Adds the created user to the "manager" group.
        6. Logs in the created user.
        Attributes:
            current_user (User): The user created for testing.
            current_condominium (Condominium): The condominium created for testing.
        """
        super().setUp()
        # create user
        self.current_user = get_user_model().objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@dummy.com",
            username="johndoe",
            password="P@ssw0rd",
        )

        # create condominium
        self.current_condominium = Condominium.objects.create(
            name="MyCondo",
            description="Good Condo",
            cnpj="15306944000169",
            address1="My Street, 10",
            address2="Wonderland",
            city="Soma City",
            state="Wellness State",
            country="BR",
            postal_code="88456123",
        )
        # assign condominium to user
        self.current_user.condominium = self.current_condominium

        # make user belong to "manager" group
        manager_group, bool_already_exists = Group.objects.get_or_create(name="manager")
        self.current_user.groups.add(manager_group)
        self.current_user.save()

        # login user
        self.client.login(username="johndoe", password="P@ssw0rd")
