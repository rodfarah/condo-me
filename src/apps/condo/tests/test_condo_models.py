from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from apps.condo.forms import CondoSetupForm
from apps.condo.models import Apartment, Block, Condominium
from apps.condo_people.tests.base_test_condo_people import CondoPeopleTestBase


class CondoModelsTest(CondoPeopleTestBase):
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
        self.first_condominium = Condominium.objects.create(
            name="MyCondo",
            description="Good Condo",
            cnpj="15.306.944/0001-69",
            address1="My Street, 10",
            address2="Wonderland",
            city="Soma City",
            state="Wellness State",
            country="BR",
            postal_code="88456123",
        )

    def test_dunder_str_returns_condominium_name(self):
        self.assertEqual(str(self.first_condominium), "MyCondo")

    def test_condominium_num_of_blocks_method_returns_correct_value(self):
        Block.objects.create(name="Fender", condominium=self.first_condominium)

        self.assertEqual(self.first_condominium.num_of_blocks(), 1)

    def test_condominium_num_of_apartment_method_returns_correct_value(self):
        block = Block.objects.create(name="Fender", condominium=self.first_condominium)

        Apartment.objects.create(
            number_or_name="102", block=block, condominium=self.first_condominium
        )

        self.assertEqual(self.first_condominium.num_of_apartments(), 1)

    def test_condominium_cnpj_no_symbols(self):
        condominium = Condominium.objects.first()
        self.assertEqual(condominium.cnpj, "15.306.944/0001-69")

    def test_condominium_invalid_cnpj_raises_validation_error(self):
        # Gets the only Condominium Object in db
        condominium = Condominium.objects.first()
        # Edit CNPJ value to an invalid value
        # 14 chars, but cnpj value not allowed in Brazil
        condominium.cnpj = "12345678901234"

        # I expect that after validations (full_clean()) the code block raises as exception
        # that I will assing as "context"
        with self.assertRaises(ValidationError) as context:
            condominium.full_clean()  # in order to execute all validations

        # context.exception is an instance of the raised exception
        # ValidationError is the class of the exception
        # context.exception.message_dict accesses the message_dict attribute
        # of the ValidationError instance.
        # context.exception.message_dict == {"cnpj": ['Please, insert a 14 digits valid CNPJ, with or without symbols.']}
        self.assertIn(
            "Please, insert a 14 digits valid CNPJ, with or without symbols.",
            context.exception.message_dict["__all__"],
        )

    def test_condominium_identical_cnpj_raises_validation_error(self):
        second_cond_data = {
            "name": "YourCondo",
            "description": "Bad Condo",
            "cnpj": "15.306.944/0001-69",  # identical to first_condominium from fixture
            "address1": "My Street, 10",
            "address2": "Wonderland",
            "city": "Soma City",
            "state": "Wellness State",
            "country": "BR",
            "postal_code": "88456123",
        }
        form = CondoSetupForm(data=second_cond_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "This CNPJ is already used. Please, consider choosing a different one.",
            form.errors.get("cnpj"),
        )
