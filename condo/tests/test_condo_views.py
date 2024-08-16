from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from condo import views


class CondoViewsTest(TestCase):
    """Condo Views Tests. Remember condo views are login_required"""

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

    def test_test_user_is_authenticated_after_set_up_login(self):
        response = self.client.get(reverse("condo:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_condo_home_view_function_is_correct(self):
        view = resolve(reverse("condo:home"))
        self.assertIs(view.func, views.home)

    def test_condo_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("condo:home"))
        self.assertEqual(response.status_code, 200)

    def test_condo_home_view_renders_correct_template(self):
        response = self.client.get(reverse("condo:home"))
        self.assertTemplateUsed(response, "condo/pages/home.html")

    def test_condo_home_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("condo:home"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(response.status_code, 302)

    def test_condo_condominium_view_function_is_correct(self):
        view = resolve(reverse("condo:condominium"))
        self.assertIs(view.func, views.condominium)

    def test_condo_common_areas_view_function_is_correct(self):
        view = resolve(reverse("condo:common_areas"))
        self.assertIs(view.func, views.common_areas)

    def test_condo_common_areas_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("condo:common_areas"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(response.status_code, 302)

    def test_condo_user_profile_view_is_correct(self):
        view = resolve(reverse("condo:user_profile_settings"))
        self.assertIs(view.func, views.user_profile_settings)

    def test_condo_user_profile_settings_view_redirects_login_page_if_user_not_logged_in(
        self,
    ):
        self.client.logout()
        response = self.client.get(reverse("condo:user_profile_settings"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(response.status_code, 302)
