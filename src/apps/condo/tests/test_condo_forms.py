from django.contrib.auth.models import Group
from django.urls import reverse

from apps.condo.forms import BlockSetupForm, CondoSetupForm
from apps.condo.models import Block, Condominium
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


class CondoSetupFormsTest(BaseFormTest):

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


class BlockSetupFormTest(BaseFormTest):
    def setUp(self):
        # include BaseFormTest setUp configuration
        super().setUp()

        self.test_block = Block.objects.create(
            name="Violet Block",
            description="Violet Block has an ocean view",
            condominium=self.test_user.condominium,
        )

    def test_blocksetupform_raises_error_if_new_block_object_name_already_exists(self):
        second_block_data = {
            "name": "Violet Block",  # identical to test_block
            "description": "Violet Block has an ocean view",
        }
        form = BlockSetupForm(data=second_block_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(
            form.errors["name"][0],
            "Block name already exists in this condominium. Please, choose a different one.",
        )

    def test_blocksetupform_accepts_valid_cleaned_name(self):
        second_block_data = {
            "name": "Jasmine Block",  # different from test_block
            "description": "Jasmine Block has a swimming pool view",
        }
        form = BlockSetupForm(data=second_block_data)
        self.assertTrue(form.is_valid())
