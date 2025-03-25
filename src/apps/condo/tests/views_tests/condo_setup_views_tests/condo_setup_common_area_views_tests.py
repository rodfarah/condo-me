"""
Testing SETUP COMMON AREA VIEWS
"""

from django.contrib.messages import get_messages
from django.urls import reverse

from apps.condo.models import CommonArea, Condominium

from .base_test_case import BaseTestCase


class SetupCommonAreaViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # create a Common Area in the condominium
        self.party_room_test = CommonArea.objects.create(
            name="Party Room",
            description="Just a common area test",
            condominium=self.current_condominium,
            opens_at="09:00",
            closes_at="20:00",
            whole_day=True,
            paid_area=True,
            price=100,
        )

    ######### SetupCommonAreaListView() #########
    def test_commonarealistview_returns_correct_queryset(self):
        response = self.client.get(reverse("condo:condo_setup_common_area_list"))

        expected_queryset = CommonArea.objects.filter(
            condominium=self.current_condominium
        )

        # verify if both querysets match
        self.assertEqual(
            list(response.context["common_area_list"]), list(expected_queryset)
        )

        # verify content of queryset and status code
        self.assertContains(response=response, text="Party Room", status_code=200)

    ######### SetupCommonAreaCreateView() #########
    def test_commonareacreateview_raises_error_message_if_user_s_condominium_does_not_exist(
        self,
    ):
        Condominium.objects.all().delete()
        response = self.client.get(reverse("condo:condo_setup_common_area_create"))

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            "In order to create a common area, you must create a condominium first",
        )

    def test_commonareacreateview_form_valid_raises_adds_error_to_form_if_common_area_name_already_exists(
        self,
    ):
        form_data = {
            "name": "Party Room",  # same as defined in setUp
            "description": "This has to fail because 'Party Room' name already exists",
            "opens_at": "11:00",
            "closes_at": "13:00",
        }

        response = self.client.post(
            path=reverse("condo:condo_setup_common_area_create"),
            data=form_data,
        )

        self.assertEqual(
            response.context["form"].errors["name"][0],
            "Common Area name already exists in this condominium. Please, choose a different one.",
        )

    def test_commonareacreateview_succeeds_if_form_is_valid(self):
        form_data = {
            "name": "Swimming Pool",
            "description": "Just another common area",
            "opens_at": "11:00",
            "closes_at": "13:00",
        }

        response = self.client.post(
            reverse("condo:condo_setup_common_area_create"), data=form_data
        )

        # verify if common area has been created in db
        self.assertTrue(
            CommonArea.objects.filter(
                name="Swimming Pool",
                condominium=self.current_condominium,
            ).exists()
        )

        # verify if form_valid raises success message to user
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Common Area has been created successfully.")

        # verify if form_valid redirects to correct url
        self.assertRedirects(
            response=response,
            expected_url=reverse("condo:condo_setup_common_area_list"),
        )
