from django.contrib.auth.models import Group

from condo.models import Apartment, Block, Condominium
from condo_people.tests.base_test_condo_people import CondoPeopleTestBase


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
            cnpj="15306944000169",
            address1="My Street, 10",
            address2="Wonderland",
            city="Soma City",
            state="Wellness State",
            country="BR",
            postal_code="88456123",
        )

    def test_dunder_str_returns_condominium_name(self):
        self.assertEqual(str(self.first_condominium), "MyCondo")

    def test_num_of_blocks_method_returns_correct_value(self):
        Block.objects.create(name="Fender", condominium=self.first_condominium)

        self.assertEqual(self.first_condominium.num_of_blocks(), 1)

    def test_num_of_apartment_method_returns_correct_value(self):
        block = Block.objects.create(name="Fender", condominium=self.first_condominium)

        Apartment.objects.create(
            number_or_name="102", block=block, condominium=self.first_condominium
        )

        self.assertEqual(self.first_condominium.num_of_apartments(), 1)
