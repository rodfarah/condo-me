"""
Testing SETUP CONDOMINIUM VIEWS
"""

from apps.condo.models import Condominium
from django.contrib.messages import get_messages
from django.urls import reverse

from .base_test_case import BaseTestCase


class SetupCondominiumViewsTest(BaseTestCase):
    def test_condo_exists_is_none_if_condominium_is_none(self):
        # remove setup condominium instance from db
        Condominium.objects.all().delete()
        # Create a get request
        url = reverse("condo:condo_setup_condominium")
        response = self.client.get(path=url)

        self.assertEqual(response.context["condo_exists"], False)

    def test_get_form_method_makes_fields_readonly_when_condoinium_exists(self):
        # get the condominium setup form page
        url = reverse("condo:condo_setup_condominium")
        response = self.client.get(path=url)

        # get form from response context
        form = response.context["form"]

        # check that form fields do not have readonly attribute
        for field in form.fields.values():
            self.assertTrue(field.widget.attrs.get("readonly"))

    def test_get_form_method_doesnt_make_fields_readonly_when_condominium_doesnt_exist(
        self,
    ):
        # Delete all existing condominium objects
        Condominium.objects.all().delete()

        # Get form page considering no condominium oject exists
        url = reverse("condo:condo_setup_condominium")
        response = self.client.get(path=url)
        form = response.context["form"]

        # verify if fields are not readonly
        for field in form.fields.values():
            self.assertFalse(field.widget.attrs.get("readonly"))

    def test_form_valid_method_sends_edit_message_if_condominium_already_exists(self):
        form_data = {
            "name": "MyBeautifulCondo",  # only different field
            "description": "Good Condo",
            "cnpj": "15306944000169",
            "address1": "My Street, 10",
            "address2": "Wonderland",
            "city": "Soma City",
            "state": "Wellness State",
            "country": "BR",
            "postal_code": "88456123",
        }

        url = reverse("condo:condo_setup_condominium")
        response = self.client.post(path=url, data=form_data, follow=True)

        # Get messages
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), "Condominium has been edited successfully")

    def test_form_valid_method_sends_create_message_if_condominium_doesnt_exist(self):
        Condominium.objects.all().delete()

        form_data = {
            "name": "MyBeautifulCondo",
            "description": "Good Condo",
            "cnpj": "15306944000169",
            "address1": "My Street, 10",
            "address2": "Wonderland",
            "city": "Soma City",
            "state": "Wellness State",
            "country": "BR",
            "postal_code": "88456123",
        }

        url = reverse("condo:condo_setup_condominium")
        response = self.client.post(path=url, data=form_data, follow=True)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), "Condominium has been created successfully")
