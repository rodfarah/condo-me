from django.test import TestCase
from django.urls import reverse


class PreloginURLsTest(TestCase):
    def test_prelogin_home_url_is_correct(self):
        home_url = reverse("apps.prelogin:home")
        self.assertEqual(home_url, "/")

    def test_prelogin_faqs_url_is_correct(self):
        faqs_url = reverse("apps.prelogin:faqs")
        self.assertEqual(faqs_url, "/faqs/")

    def test_prelogin_features_url_is_correct(self):
        features_url = reverse("apps.prelogin:features")
        self.assertEqual(features_url, "/features/")

    def test_prelogin_pricing_url_is_correct(self):
        pricing_url = reverse("apps.prelogin:pricing")
        self.assertEqual(pricing_url, "/pricing/")

    def test_prelogin_about_url_is_correct(self):
        about_url = reverse("apps.prelogin:about")
        self.assertEqual(about_url, "/about/")
