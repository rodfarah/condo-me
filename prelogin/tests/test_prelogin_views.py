from django.test import TestCase
from django.urls import resolve, reverse

from .. import views


class PreloginViewsTest(TestCase):
    def test_prelogin_home_view_function_is_correct(self):
        view = resolve(reverse("prelogin:home"))
        self.assertIs(view.func, views.home)

    def test_prelogin_faqs_view_function_is_correct(self):
        view = resolve(reverse("prelogin:faqs"))
        self.assertIs(view.func, views.faqs)

    def test_prelogin_features_function_is_correct(self):
        view = resolve(reverse("prelogin:features"))
        self.assertIs(view.func, views.features)

    def test_prelogin_pricing_function_is_correct(self):
        view = resolve(reverse("prelogin:pricing"))
        self.assertIs(view.func, views.pricing)
