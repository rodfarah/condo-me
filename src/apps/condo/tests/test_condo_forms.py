from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.urls import reverse

from apps.condo.forms import CondoSetupForm
from apps.condo.models import Apartment, Block, Condominium
from apps.condo_people.tests.base_test_condo_people import CondoPeopleTestBase


class BaseFormTest(CondoPeopleTestBase):
    """
    BaseFormTest is a test case class that inherits from CondoPeopleTestBase.
    It sets up a test environment for testing forms related to condominiums.
    Methods:
        setUp():
            Creates a test user, assigns the user to the 'manager' group, logs in the user,
            and creates a sample condominium for testing purposes.
    """

    def setUp(self):
        # create a test user
        self.test_user = self.create_test_user()
        # get 'manager' group
        manager_group = Group.objects.get(name="manager")
        # concede "manager group" to test_user
        self.test_user.groups.add(manager_group)
        # create the first condominium
        test_condominium = Condominium.objects.create(
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
        # associate test_condominium with user.condominium
        self.test_user.condominium = test_condominium
        self.test_user.save()

        self.login_test_user()


class CondoSetupCondominiumFormsTest(BaseFormTest):

    def test_unique_condo_cnpj_gets_status_code_302_form(self):
        condo2_data = {
            "name": "YourCondo",
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

    def test_clean_cnpj_propagates_model_validation_error(self):
        condo2_data = {
            "name": "YourCondo",  # different name from condo1 in fixture
            "description": "Bad Condo",
            "cnpj": "00000000000000",  # invalid CNPJ, different from condo1 in fixture
            "address1": "Your Street, 20",
            "address2": "NightmareLand",
            "city": "Ugly City",
            "state": "Sick State",
            "country": "BR",
            "postal_code": "12345678",
        }
        form = CondoSetupForm(data=condo2_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cnpj", form.errors)
        # verify error message matches what model validation must raise
        self.assertEqual(
            form.errors["cnpj"][0],
            "Please, insert a 14 digits valid CNPJ, with or without symbols.",
        )


class CondoSetupApartmentFormsTest(BaseFormTest):
    def setUp(self):
        super().setUp()
        self.test_block = Block.objects.create(
            number_or_name="Violet",
            description="Just a test block",
            condominium=self.test_user.condominium,
        )

    def test_apartment_setup_form_raises_value_error_if_user_create_apartment_without_condominium(
        self,
    ):
        # delete test condominium
        self.test_user.condominium.delete()
        self.test_user.condominium = None
        self.test_user.save()

        # try to access apartment create view

        response = self.client.get(
            reverse(
                "condo:condo_setup_apartment_create",
                kwargs={"block_id": self.test_block.id},
            )
        )

        # should redirect with error message
        self.assertEqual(response.status_code, 302)
        # check specific error message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("must create a condominium first", str(messages[0]))

    def test_apartment_setup_form_raises_validation_error_when_creating_apartment_with_duplicated_number_or_name(
        self,
    ):
        # create first apartment tester
        Apartment.objects.create(
            condominium=self.test_user.condominium,
            block=self.test_block,
            number_or_name="102",
        )
        # count apartments before attempt
        apartments_count = Apartment.objects.count()
        # create second apartment with identical name, via HTTP request
        form_data = {"number_or_name": "102"}
        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_create",
                kwargs={
                    "block_id": self.test_block.id,
                },
            ),
            data=form_data,
        )
        # form should be invalid and return to same page
        self.assertEqual(response.status_code, 200)

        # no new apartment was created
        self.assertEqual(Apartment.objects.count(), apartments_count)

        # verify form error in context
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Apartment number (or name) already exists in this block. Please, choose a different one.",
            form.errors["number_or_name"],
        )


class CondoSetupApartmentMultipleFormsTest(BaseFormTest):
    def setUp(self):
        super().setUp()
        self.test_block = Block.objects.create(
            number_or_name="Violet",
            description="Just a test block",
            condominium=self.test_user.condominium,
        )

    def test_apartment_multiple_setup_form_raises_error_if_last_floor_is_higher_then_first_floor(
        self,
    ):
        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.test_block.id},
        )
        form_data = {"first_floor": 2, "last_floor": 1, "apartments_per_floor": 3}
        # make request
        response = self.client.post(path=url, data=form_data)

        self.assertFormError(
            form=response.context["form"],
            field="last_floor",
            errors=[
                "Last floor number must be equal or higher than first floor number"
            ],
        )
