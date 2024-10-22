from django.urls import reverse

from .base_test_condo_people import TokenTestBase


class CondoPeopleURLsTest(TokenTestBase):
    def test_condo_people_register_url_is_correct(self):
        registration_token = self.create_test_token()
        url = reverse(
            "condo_people:register", kwargs={"token": registration_token.token}
        )
        self.assertEqual(url, f"/condo_people/register/{registration_token.token}")

    def test_condo_people_register_create_url_is_correct(self):
        url = reverse("condo_people:register_create")
        self.assertEqual(url, "/condo_people/register/create/")

    def test_condo_people_login_url_is_correct(self):
        url = reverse("condo_people:login")
        self.assertEqual(url, "/condo_people/login/")

    def test_condo_people_login_create_url_is_correct(self):
        url = reverse("condo_people:login_create")
        self.assertEqual(url, "/condo_people/login/create/")

    def test_condo_people_logout_url_is_correct(self):
        url = reverse("condo_people:logout")
        self.assertEqual(url, "/condo_people/logout/")

    def test_condo_people_password_change_url_is_correct(self):
        url = reverse("condo_people:password_change")
        self.assertEqual(url, "/condo_people/password-change/")

    def test_condo_people_password_reset_url_is_correct(self):
        url = reverse("condo_people:password_reset")
        self.assertEqual(url, "/condo_people/password-reset/")

    def test_condo_people_password_reset_done_url_is_correct(self):
        url = reverse("condo_people:password_reset_done")
        self.assertEqual(url, "/condo_people/password-reset/done/")

    def test_condo_people_password_reset_confirm_url_is_correct(self):
        url = reverse(
            "condo_people:password_reset_confirm",
            kwargs={"uidb64": "dummy_uidb64", "token": "dummy_token"},
        )
        self.assertEqual(url, "/condo_people/password-reset/dummy_uidb64/dummy_token/")

    def test_condo_people_password_reset_complete_url_is_correct(self):
        url = reverse("condo_people:password_reset_complete")
        self.assertEqual(url, "/condo_people/password-reset/complete/")
