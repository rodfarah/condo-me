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

    def test_prelogin_about_function_is_correct(self):
        view = resolve(reverse("prelogin:about"))
        self.assertIs(view.func, views.about)

    def test_prelogin_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("prelogin:home"))
        self.assertEqual(response.status_code, 200)

    def test_prelogin_home_view_renders_correct_template(self):
        response = self.client.get(reverse("prelogin:home"))
        self.assertTemplateUsed(response, "prelogin/pages/home.html")

    def test_prelogin_faqs_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("prelogin:faqs"))
        self.assertEqual(response.status_code, 200)

    def test_prelogin_faqs_view_renders_correct_template(self):
        response = self.client.get(reverse("prelogin:faqs"))
        self.assertTemplateUsed(response, "prelogin/pages/faqs.html")

    def test_prelogin_features_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("prelogin:features"))
        self.assertEqual(response.status_code, 200)

    def test_prelogin_features_view_renders_correct_template(self):
        response = self.client.get(reverse("prelogin:features"))
        self.assertTemplateUsed(response, "prelogin/pages/features.html")

    def test_prelogin_pricing_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("prelogin:pricing"))
        self.assertEqual(response.status_code, 200)

    def test_prelogin_pricing_view_renders_correct_template(self):
        response = self.client.get(reverse("prelogin:pricing"))
        self.assertTemplateUsed(response, "prelogin/pages/pricing.html")

    def test_prelogin_about_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("prelogin:about"))
        self.assertEqual(response.status_code, 200)

    def test_prelogin_about_view_renders_correct_template(self):
        response = self.client.get(reverse("prelogin:about"))
        self.assertTemplateUsed(response, "prelogin/pages/about.html")
