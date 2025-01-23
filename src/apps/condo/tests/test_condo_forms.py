from django.contrib.auth.models import Group
from django.urls import reverse

from apps.condo.models import Condominium
from apps.condo_people.tests.base_test_condo_people import CondoPeopleTestBase


class CondoFormsTest(CondoPeopleTestBase):
    def setUp(self):
        # create a test user
        self.test_user = self.create_test_user()
        # get 'manager' group
        manager_group = Group.objects.get(name="manager")
        # concede "manager group" to test_user
        self.test_user.groups.add(manager_group)
        self.test_user.save()

        # log in test_user
        self.login_test_user()

        # create the first condominium
        Condominium.objects.create(
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

    def test_condo_name_already_used_return_validation_error_form(self):

        condo2_data = {
            "name": "MyCondo",  # same name as condo1 from fixture
            "description": "Bad Condo",
            "cnpj": "15306944000169",
            "address1": "Your Street, 20",
            "address2": "NightmareLand",
            "city": "Ugly City",
            "state": "Sick State",
            "country": "BR",
            "postal_code": "12345678",
        }

        response = self.client.post(
            path=reverse("condo:condo_setup_condominium"), data=condo2_data
        )
        self.assertIn(
            "Condominium name already exists. Please, choose a different one.",
            response.content.decode("utf-8"),
        )

    def test_unique_condo_name_and_cnpj_gets_status_code_302_form(self):
        condo2_data = {
            "name": "YourCondo",  # different name from condo1 in fixture
            "description": "Bad Condo",
            "cnpj": "39053118000113",  # Valid CNPJ, different from condo1 in fixture
            "address1": "Your Street, 20",
            "address2": "NightmareLand",
            "city": "Ugly City",
            "state": "Sick State",
            "country": "BR",
            "postal_code": "12345678",
        }

        response = self.client.post(
            path=reverse("condo:condo_setup_condominium"),
            data=condo2_data,
        )

        condo_exists = Condominium.objects.filter(name__iexact="YourCondo").exists()

        self.assertTrue(condo_exists)

        self.assertRedirects(
            response,
            reverse("condo:condo_setup_home"),
            status_code=302,
        )
