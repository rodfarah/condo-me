from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import resolve, reverse
from django.utils import timezone

from apps.condo_people import views
from apps.purchase.models import RegistrationToken

from .base_test_condo_people import CondoPeopleTestBase, TokenTestBase


class CondoPeopleViewsTest(TokenTestBase, CondoPeopleTestBase):
    # REGISTER VIEW TESTS
    def test_condo_people_register_view_function_is_correct(self):
        register_token = self.create_test_token()
        view = resolve(
            reverse("condo_people:register", kwargs={"token": register_token.token})
        )
        self.assertIs(view.func, views.register_view)

    def test_condo_people_register_view_renders_correct_template(self):
        register_token = self.create_test_token()
        response = self.client.get(
            reverse("condo_people:register", kwargs={"token": register_token.token})
        )
        self.assertTemplateUsed(response, "condo_people/registration/register.html")

    def test_invalid_token_redirects_to_invalid_token_view(self):
        # create a test token
        register_token = self.create_test_token()
        # get it from db
        expired_token = RegistrationToken.objects.get(token=register_token.token)
        # turn it to an "expired" token
        expired_token.expires_at = timezone.now() - timedelta(2)
        expired_token.save()
        response = self.client.post(
            path=reverse("condo_people:register", kwargs={"token": expired_token.token})
        )
        self.assertRedirects(
            response=response, expected_url=reverse("condo_people:invalid_token")
        )

    def test_token_doesnt_exist_removes_session_items_redirects_invalid_token_view(
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

        session = self.client.session
        session["register_form_data"] = form_data
        session["token"] = "testingAnything"
        session.save()

        # send an invalid token (does not exist) as kwarg
        response = self.client.post(
            reverse(
                "condo_people:register",
                kwargs={
                    "token": session.get("token"),
                },
            )
        )
        self.assertRedirects(
            response=response, expected_url=reverse("condo_people:invalid_token")
        )

        # must reload session
        session = self.client.session

        # check if session data was removed
        self.assertNotIn("register_form_data", session)
        self.assertNotIn("token", session)

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
        register_token = self.create_test_token()
        session = self.client.session
        session["token"] = register_token.token
        session.save()

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
        register_token = self.create_test_token()
        session = self.client.session
        session["token"] = register_token.token
        session.save()

        response = self.client.post(
            path=reverse("condo_people:register_create"), data=form_data
        )
        self.assertRedirects(
            response,
            reverse("condo_people:register", kwargs={"token": session.get("token")}),
            status_code=302,
        )

    # LOGIN VIEW TESTS
    def test_condo_people_login_view_function_is_correct(self):
        view = resolve(reverse("condo_people:login"))
        self.assertIs(view.func, views.login_view)

    def test_condo_people_login_view_redirects_condo_home_if_user_already_athenticated(
        self,
    ):
        self.create_test_user()
        self.login_test_user()
        response = self.client.get(reverse("condo_people:login"))
        self.assertRedirects(response, reverse("condo:home"), status_code=302)

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

    def test_condo_people_login_create_user_is_none_if_username_not_in_db(self):
        # no user created. Just login.
        login_data = {"username": "johndoe", "password": "DummyTest"}
        response = self.client.post(
            reverse("condo_people:login_create"), data=login_data
        )
        response = self.client.get(reverse("condo_people:login"))
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any(
                msg.message == "Invalid username and/or password. Please, try again."
                for msg in messages
            )
        )

    def test_condo_people_login_create_authenticates_active_user_if_valid_data_and_redirects(
        self,
    ):
        self.create_test_user()
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

    def test_condo_people_login_create_renders_wright_template_if_not_valid_data(
        self,
    ):
        self.create_test_user()
        # Invalid data
        form_data = {"username": "", "password": "BetweenTheBar"}
        response = self.client.post(
            reverse("condo_people:login_create"), data=form_data
        )
        # check if view renders correct template
        self.assertTemplateUsed(response, "condo_people/registration/login.html")

    def test_condo_people_login_create_view_sends_error_message_if_not_active_user(
        self,
    ):
        self.create_test_user(is_active=False)
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

    def test_condo_people_login_create_view_error_msg_and_redirects_if_not_authenticated_user(
        self,
    ):
        self.create_test_user()
        # wrong password
        form_data = {"username": "elliotsmith", "password": "AnyDumb_pswd"}
        response = self.client.post(
            reverse("condo_people:login_create"), data=form_data
        )
        # user is NOT authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # ensure redirect
        self.assertRedirects(response, reverse("condo_people:login"))
        # check if error message is rendered
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                msg.message == "Invalid username and/or password. Please, try again."
                for msg in messages
            )
        )

    # LOGOUT VIEW TESTS
    def test_condo_people_logout_view_is_correct(self):
        view = resolve(reverse("condo_people:logout"))
        self.assertIs(view.func, views.logout_view)

    def test_condo_people_logout_view_logout_and_redirects_login_view_if_post_method(
        self,
    ):
        # Create user in db
        self.create_test_user()
        # login user
        login_request = self.login_test_user()
        self.assertTrue(login_request)
        # logout user
        response = self.client.post(reverse("condo_people:logout"))
        # check if user session is deleted
        self.assertFalse("_auth_user_id" in self.client.session)

        # Follow redirection and check if login page is rendered
        response = self.client.get(reverse("condo_people:login"))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "condo_people/registration/login.html")

    def test_condo_people_logout_view_only_redirects_if_get_method(self):
        self.create_test_user()
        self.login_test_user()
        # user tries to logout via GET method (instead of POST)
        # follow=True deals with multiple redirections
        response = self.client.get(reverse("condo_people:logout"), follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse("condo:home"),
        )
