from django.urls import reverse

from .base_test_condo_people import CondoPeopleTestBase, TokenTestBase


class UserRegisterFormUnitTest(CondoPeopleTestBase, TokenTestBase):
    def test_email_already_used_raises_validation_error(self):
        # create test user (elliot@smith.com)
        self.create_test_user()
        form_data = {
            "first_name": "Johanna",
            "last_name": "Warren",
            # e-mail already in use by other user
            "email": "elliot@smith.com",
            "username": "johannawarren",
            "password1": "wefell",
            "password2": "wefell",
            "is_active": True,
        }
        register_token = self.create_test_token()
        session = self.client.session
        session["token"] = register_token.token
        session.save()

        response = self.client.post(
            path=reverse("apps.condo_people:register_create"), data=form_data
        )
        self.assertIn(
            response.content.decode("utf-8"),
            "This e-mail address has been already used. Please, choose a different one.",
        )
