from .base_test_condo_people import CondoPeopleTestBase


class UserModelTest(CondoPeopleTestBase):
    def test_dunder_str_returns_firstname_lastname(self):
        test_user = self.create_test_user()
        self.assertEqual(str(test_user), "Elliot Smith")
