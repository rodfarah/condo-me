from django.test import TestCase
from django.urls import resolve, reverse

from .. import views


class CondoPeopleViewsTest(TestCase):
    def test_condo_people_register_view_function_is_correct(self):
        view = resolve(reverse("condo_people:register"))
        self.assertIs(view.func, views.register_view)

    def test_condo_people_register_create_view_function_is_correct(self):
        view = resolve(reverse("condo_people:register_create"))
        self.assertIs(view.func, views.register_create)

    def test_condo_people_login_view_function_is_correct(self):
        view = resolve(reverse("condo_people:login"))
        self.assertIs(view.func, views.login_view)
