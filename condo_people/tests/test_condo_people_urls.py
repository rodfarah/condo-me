from django.test import TestCase
from django.urls import reverse


class CondoPeopleURLsTest(TestCase):
    def test_condo_people_register_url_is_correct(self):
        url = reverse("condo_people:register")
        self.assertEqual(url, "/condo_people/register/")

    def test_condo_people_register_create_url_is_correct(self):
        url = reverse("condo_people:register_create")
        self.assertEqual(url, "/condo_people/register/create/")

    def test_condo_people_login_url_is_correct(self):
        url = reverse("condo_people:login")
        self.assertEqual(url, "/condo_people/login/")

    def test_condo_people_login_create_url_is_correct(self):
        url = reverse("condo_people:login_create")
        self.assertEqual(url, "/condo_people/login/create/")

    def test_condo_people_logout_url_is_correct(self):
        url = reverse("condo_people:logout")
        self.assertEqual(url, "/condo_people/logout/")
