from django.contrib.auth import get_user_model
from django.test import TestCase


class CondoViewsTest(TestCase):
    """Condo Views Tests. Please, consider condo views are login_required"""

    # setup for starting each test
    def setUp(self) -> None:
        get_user_model().objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@dummy.com",
            username="johndoe",
            password="P@ssw0rd",
        )
        self.client.login(username="johndoe", password="P@ssw0rd")
        return super().setUp()

    def test_form_receives_condo_info_via_get_method_views(self):
        pass
