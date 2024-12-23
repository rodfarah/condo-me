from django.test import TestCase
from django.urls import reverse


class CondoURLsTest(TestCase):
    def test_condo_home_url_is_correct(self):
        home_url = reverse("condo:home")
        self.assertEqual(home_url, "/condo/")

    def test_condo_condominium_url_is_correct(self):
        condominium_url = reverse("condo:condominium")
        self.assertEqual(condominium_url, "/condo/condominium/")

    def test_common_areas_url_is_correct(self):
        common_areas_url = reverse("condo:common_areas")
        self.assertEqual(common_areas_url, "/condo/common_areas/")

    def test_user_profile_settings_url_is_correct(self):
        user_prof_set_url = reverse("condo:user_profile_settings")
        self.assertEqual(user_prof_set_url, "/condo/user/profile/settings/")
