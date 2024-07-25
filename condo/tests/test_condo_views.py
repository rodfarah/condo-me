from django.test import TestCase
from django.urls import resolve, reverse

from .. import views


class CondoViewsTest(TestCase):
    def test_condo_home_view_function_is_correct(self):
        view = resolve(reverse("condo:home"))
        self.assertIs(view.func, views.home)

    def test_condo_condominium_view_function_is_correct(self):
        view = resolve(reverse("condo:condominium"))
        self.assertIs(view.func, views.condominium)

    def test_condo_common_areas_view_function_is_correct(self):
        view = resolve(reverse("condo:common_areas"))
        self.assertIs(view.func, views.common_areas)
