from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from apps.condo import views


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

    # Basic authentication test
    def test_user_is_authenticated_after_test_set_up_login(self):
        response = self.client.get(reverse("apps.condo:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # HOME VIEW TESTS
    def test_condo_home_view_function_is_correct(self):
        view = resolve(reverse("apps.condo:home"))
        self.assertIs(view.func, views.home)

    def test_condo_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("apps.condo:home"))
        self.assertEqual(response.status_code, 200)

    def test_condo_home_view_renders_correct_template(self):
        response = self.client.get(reverse("apps.condo:home"))
        self.assertTemplateUsed(response, "condo/pages/home.html")

    def test_condo_home_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("apps.condo:home"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/",
        )

    # CONDOMINIUM VIEW TESTS
    def test_condo_condominium_view_function_is_correct(self):
        view = resolve(reverse("apps.condo:condominium"))
        self.assertIs(view.func, views.condominium)

    def test_condo_condominium_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("apps.condo:condominium"))
        self.assertEqual(response.status_code, 200)

    def test_condo_condominium_view_renders_correct_template(self):
        response = self.client.get(reverse("apps.condo:condominium"))
        self.assertTemplateUsed(response, "condo/pages/condominium.html")

    def test_condo_condominium_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("apps.condo:condominium"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/condominium/",
        )

    # COMMON AREAS VIEW TESTS
    def test_condo_common_areas_view_function_is_correct(self):
        view = resolve(reverse("apps.condo:common_areas"))
        self.assertIs(view.func, views.common_areas)

    def test_condo_common_areas_view_renders_correct_template(self):
        response = self.client.get(reverse("apps.condo:common_areas"))
        self.assertTemplateUsed(response, "condo/pages/common_areas.html")

    def test_condo_common_areas_view_returns_status_200_ok(self):
        response = self.client.get(reverse("apps.condo:common_areas"))
        self.assertIs(response.status_code, 200)

    def test_condo_common_areas_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("apps.condo:common_areas"))
        # user not logged in, redirects (302) to login page
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/condominium/common_areas/",
        )

    # USER PROFILE VIEW TESTS
    def test_condo_user_profile_view_is_correct(self):
        view = resolve(reverse("apps.condo:user_profile_settings"))
        self.assertIs(view.func, views.user_profile_settings)

    def test_condo_user_profile_view_renders_correct_template(self):
        response = self.client.get(reverse("apps.condo:user_profile_settings"))
        self.assertTemplateUsed(response, "condo/pages/user_profile.html")

    def test_condo_user_profile_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("apps.condo:user_profile_settings"))
        self.assertIs(response.status_code, 200)

    def test_condo_user_profile_settings_view_redirects_login_page_if_user_not_logged_in(
        self,
    ):
        self.client.logout()
        response = self.client.get(reverse("apps.condo:user_profile_settings"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/user/profile/settings/",
        )
