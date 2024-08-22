from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import resolve, reverse

from condo_people import views


class CondoPeopleViewsTest(TestCase):
    # REGISTER VIEW TESTS
    def test_condo_people_register_view_function_is_correct(self):
        view = resolve(reverse("condo_people:register"))
        self.assertIs(view.func, views.register_view)

    def test_condo_people_register_view_renders_correct_template(self):
        response = self.client.get(reverse("condo_people:register"))
        self.assertTemplateUsed(response, "condo_people/registration/register.html")

    # REGISTER CREATE TESTS
    def test_condo_people_register_create_view_function_is_correct(self):
        view = resolve(reverse("condo_people:register_create"))
        self.assertIs(view.func, views.register_create)

    def test_condo_people_register_create_view_raises_404_if_get_method(self):
        response = self.client.get(reverse("condo_people:register_create"))
        self.assertEqual(response.status_code, 404)

    def test_condo_people_register_create_view_saves_and_redirects_to_login_if_form_is_valid(
        self,
    ):
        form_data = {
            "first_name": "Elliot",
            "last_name": "Smith",
            "email": "elliot@smith.com",
            "username": "elliotsmith",
            "password1": "BetweenTheBars",
            "password2": "BetweenTheBars",
        }
        response = self.client.post(
            path=reverse("condo_people:register_create"), data=form_data
        )
        # Check if User has been saved
        self.assertTrue(
            get_user_model().objects.filter(username="elliotsmith").exists()
        )
        # Check if register create view redirects to login view
        self.assertRedirects(response, reverse("condo_people:login"), status_code=302)

    def test_condo_people_register_create_view_redirects_to_register_view_if_invalid_data(
        self,
    ):
        form_data = {
            "first_name": "Elliot",
            "last_name": "Smith",
            "email": "elliot@smith.com",
            "username": "elliotsmith",
            "password1": "betweenTheBars",
            # invalid data
            "password2": "",
        }
        response = self.client.post(
            path=reverse("condo_people:register_create"), data=form_data
        )
        self.assertRedirects(
            response, reverse("condo_people:register"), status_code=302
        )

    # LOGIN VIEW TESTS
    def test_condo_people_login_view_function_is_correct(self):
        view = resolve(reverse("condo_people:login"))
        self.assertIs(view.func, views.login_view)

    def test_condo_people_login_view_renders_correct_template(self):
        response = self.client.get(reverse("condo_people:login"))
        self.assertTemplateUsed(response, "condo_people/registration/login.html")

    # LOGIN CREATE VIEW TESTS
    def test_condo_people_login_create_view_is_correct(self):
        view = resolve(reverse("condo_people:login_create"))
        self.assertIs(view.func, views.login_create)

    def test_condo_people_login_create_returns_404_if_get_method(self):
        response = self.client.get(reverse("condo_people:login_create"))
        self.assertEqual(response.status_code, 404)

    def test_condo_people_login_create_authenticates_active_user_if_valid_data_and_redirects(
        self,
    ):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            first_name="Elliot",
            last_name="Smith",
            email="elliot@smith.com",
            username="elliotsmith",
            password="BetweenTheBars",
        )
        form_data = {"username": "elliotsmith", "password": "BetweenTheBars"}
        response = self.client.post(
            reverse("condo_people:login_create"), data=form_data
        )
        # Check if user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        # Check if user is logged in (session exists)
        self.assertTrue(response.wsgi_request.session.exists)
        # check if view redirects correctly
        self.assertRedirects(response, reverse("condo:home"), status_code=302)

    def test_condo_people_login_create_view_sends_error_message_if_not_active_user(
        self,
    ):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            first_name="Elliot",
            last_name="Smith",
            email="elliot@smith.com",
            username="elliotsmith",
            password="BetweenTheBars",
            is_active=False,
        )
        # first response, related to login_create view
        response = self.client.post(
            reverse("condo_people:login_create"),
            data={"username": "elliotsmith", "password": "BetweenTheBars"},
        )
        # second response, related to login view (previously redirected from login_create view)
        response = self.client.get(reverse("condo_people:login"))
        # getting message list
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(any(msg.message == "Disabled Account" for msg in messages))

    def test_condo_people_login_create_renders_wright_template_if_not_valid_data(
        self,
    ):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            first_name="Elliot",
            last_name="Smith",
            email="elliot@smith.com",
            username="elliotsmith",
            password="BetweenTheBars",
        )
        # Invalid data
        form_data = {"username": "", "password": "BetweenTheBar"}
        response = self.client.post(
            reverse("condo_people:login_create"), data=form_data
        )
        # check if view renders correct template
        self.assertTemplateUsed(response, "condo_people/registration/login.html")

    # LOGOUT VIEW TESTS
    def test_condo_people_logout_view_is_correct(self):
        view = resolve(reverse("condo_people:logout"))
        self.assertIs(view.func, views.logout_view)
