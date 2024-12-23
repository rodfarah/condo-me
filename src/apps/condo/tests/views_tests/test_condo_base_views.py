"""
'test_condo_base_views' are applied to the first page user will get when logged in.
These tests are DIFFERENT from 'test_setup_condominium_views', which are applied to the condominium
configuration page accessible only to 'manager' users.
"""

from apps.condo import views
from apps.condo.models import Condominium
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse


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
        response = self.client.get(reverse("condo:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # HOME VIEW TESTS
    def test_condo_home_view_function_is_correct(self):
        view = resolve(reverse("condo:home"))
        self.assertIs(view.func, views.home)

    def test_condo_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("condo:home"))
        self.assertEqual(response.status_code, 200)

    def test_condo_home_view_renders_correct_template(self):
        response = self.client.get(reverse("condo:home"))
        self.assertTemplateUsed(response, "condo/pages/home_pages/welcome.html")

    def test_condo_home_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("condo:home"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/",
        )

    def test_condo_home_view_send_condo_cover_url_as_context_if_condo_cover_exists(
        self,
    ):
        current_user = get_user_model().objects.first()
        condo = Condominium.objects.create(
            name="YourCondo",
            description="Bad Condo",
            cnpj="39053118000113",  # Valid CNPJ
            address1="Your Street, 20",
            address2="NightmareLand",
            city="Ugly City",
            state="Sick State",
            country="BR",
            postal_code="12345678",
            cover="test_image.jpg",
        )
        current_user.condominium = condo
        current_user.save()
        response = self.client.get(reverse("condo:home"))

        self.assertEqual(
            response.context["condo_cover"],
            f"{condo.cover.name}",
        )

    # CONDOMINIUM VIEW TESTS
    def test_condo_condominium_view_function_is_correct(self):
        view = resolve(reverse("condo:condominium"))
        self.assertIs(view.func, views.condominium)

    def test_condo_condominium_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("condo:condominium"))
        self.assertEqual(response.status_code, 200)

    def test_condo_condominium_view_renders_correct_template(self):
        response = self.client.get(reverse("condo:condominium"))
        self.assertTemplateUsed(response, "condo/pages/home_pages/condominium.html")

    def test_condo_condominium_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("condo:condominium"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/condominium/",
        )

    # COMMON AREAS VIEW TESTS
    def test_condo_common_areas_view_function_is_correct(self):
        view = resolve(reverse("condo:common_areas"))
        self.assertIs(view.func, views.common_areas)

    def test_condo_common_areas_view_renders_correct_template(self):
        response = self.client.get(reverse("condo:common_areas"))
        self.assertTemplateUsed(response, "condo/pages/home_pages/common_areas.html")

    def test_condo_common_areas_view_returns_status_200_ok(self):
        response = self.client.get(reverse("condo:common_areas"))
        self.assertIs(response.status_code, 200)

    def test_condo_common_areas_view_redirects_login_page_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("condo:common_areas"))
        # user not logged in, redirects (302) to login page
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/common_areas/",
        )

    # USER PROFILE VIEW TESTS
    def test_condo_user_profile_settings_view_is_correct(self):
        view = resolve(reverse("condo:user_profile_settings"))
        self.assertIs(view.func, views.user_profile_settings)

    def test_condo_user_profile_settings_view_renders_correct_template(self):
        response = self.client.get(reverse("condo:user_profile_settings"))
        self.assertTemplateUsed(response, "condo/pages/home_pages/user_profile.html")

    def test_condo_user_profile_settings_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("condo:user_profile_settings"))
        self.assertIs(response.status_code, 200)

    def test_condo_user_profile_settings_view_redirects_login_page_if_user_not_logged_in(
        self,
    ):
        self.client.logout()
        response = self.client.get(reverse("condo:user_profile_settings"))
        # user not logged in, redirects (302) to login page
        self.assertEqual(
            response.url,
            "/condo_people/login?redirect_to=/condo/user/profile/settings/",
        )
