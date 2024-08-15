from django.test import TestCase
from django.urls import reverse


class PreloginURLsTest(TestCase):
    def test_prelogin_home_url_is_correct(self):
        home_url = reverse("prelogin:home")
        self.assertEqual(home_url, "/")

    def test_prelogin_faqs_url_is_correct(self):
        faqs_url = reverse("prelogin:faqs")
        self.assertEqual(faqs_url, "/faqs/")

    def test_prelogin_features_url_is_correct(self):
        features_url = reverse("prelogin:features")
        self.assertEqual(features_url, "/features/")

    def test_prelogin_pricing_url_is_correct(self):
        pricing_url = reverse("prelogin:pricing")
        self.assertEqual(pricing_url, "/pricing/")

    def test_prelogin_about_url_is_correct(self):
        about_url = reverse("prelogin:about")
        self.assertEqual(about_url, "/about/")
