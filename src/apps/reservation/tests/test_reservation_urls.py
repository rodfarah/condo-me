from django.test import TestCase
from django.urls import reverse


class ReservationURLsTest(TestCase):
    def test_reservation_url_is_correct(self):
        reservation_url = reverse("apps.reservation:reserve")
        self.assertEqual(reservation_url, "/reservation/")
