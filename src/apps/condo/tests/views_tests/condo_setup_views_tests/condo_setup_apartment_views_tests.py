"""
Testing SETUP APARTMENT VIEWS
"""

import uuid

from django.contrib.messages import get_messages
from django.test.client import Client
from django.urls import reverse

from apps.condo.models import Apartment, Block, Condominium

from .base_test_case import BaseTestCase


class SetupApartmentViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # create a block to the condominium
        self.block_one = Block.objects.create(
            number_or_name="Block One",
            description="First Block",
            condominium=self.current_condominium,
        )
        # create an apartment in this block
        self.apartment_one_o_one = Apartment.objects.create(
            number_or_name="101",
            block=self.block_one,
            condominium=self.current_condominium,
        )

    ######### SetupApartmentsByBlockListView() #########

    def test_apartmentsbyblocklistview_raises_error_if_block_doesnot_exist(self):
        block_id = uuid.uuid4()  # valid, but inexistent
        response = self.client.get(
            reverse(
                "condo:condo_setup_apartment_list_by_block",
                kwargs={"block_id": block_id},
            ),
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertIn(
            str(messages[0]),
            "The requested block does not exist or does not belong to your condominium.",
        )
        self.assertRedirects(
            response, reverse("condo:condo_setup_blocks_to_apartments")
        )

    def test_apartmentsbyblocklistview_get_queryset_properly(self):
        block_id = self.block_one.pk

        expected_queryset = Apartment.objects.filter(
            condominium=self.current_condominium, block=self.block_one
        )

        response = self.client.get(
            reverse(
                "condo:condo_setup_apartment_list_by_block",
                kwargs={"block_id": block_id},
            )
        )

        self.assertQuerySetEqual(
            list(response.context["apartments_in_block"]),
            list(expected_queryset),
            ordered=False,
        )

    ######### SetupApartmentCreateView() #########

    def test_apartmentcreateview_raises_error_if_block_does_not_exist(self):
        block_id = uuid.uuid4()  # valid, but inexistent

        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_create", kwargs={"block_id": block_id}
            ),
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            "You are trying to create apartments in a block that does not exist",
        )
        self.assertRedirects(
            response, reverse("condo:condo_setup_blocks_to_apartments")
        )

    def test_apartmentcreateview_success_url_returns_correct_url(self):
        # create another apartment
        form_data = {"number_or_name": "102"}
        response = self.client.post(
            path=reverse(
                "condo:condo_setup_apartment_create",
                kwargs={"block_id": self.block_one.pk},
            ),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse(
                "condo:condo_setup_apartment_list_by_block",
                kwargs={"block_id": self.block_one.pk},
            ),
        )

    def test_apartmentcreateview_redirects_ok_and_raises_success_message_if_request_is_ok(
        self,
    ):
        # create another apartment
        form_data = {"number_or_name": "302"}
        response = self.client.post(
            path=reverse(
                "condo:condo_setup_apartment_create",
                kwargs={"block_id": self.block_one.pk},
            ),
            data=form_data,
            follow=False,  # in order to confirm redirect status code
        )
        # verify redirection
        self.assertEqual(response.status_code, 302)

        # verify redirect url
        expected_url = reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.block_one.pk},
        )
        self.assertRedirects(response, expected_url=expected_url)

        # verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Apartment has been created successfully.", str(messages[0]))

        # verify apartment has been created
        self.assertTrue(
            Apartment.objects.filter(
                number_or_name="302",
                block=self.block_one,
                condominium=self.current_condominium,
            ).exists()
        )

    ######### SetupApartmentDeleteView() #########
    def test_apartmentdeleteview_sends_correct_context_to_template(self):
        # make a delete request
        response = self.client.get(
            path=reverse(
                "condo:condo_setup_apartment_delete",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            ),
            follow=False,
        )
        # verify context data
        self.assertEqual(response.context["apartment_id"], self.apartment_one_o_one.pk)
        self.assertEqual(response.context["apartment_num_or_name"], "101")
        self.assertEqual(response.context["apartment_block"], self.block_one)

    def test_apartmentdeleteview_redirects_success_url_and_raises_success_message(self):
        # verify if apartment exists
        current_apartment = Apartment.objects.get(
            number_or_name="101",
            block=self.block_one,
            condominium=self.current_condominium,
        )
        self.assertTrue(current_apartment)
        # make a delete request
        response = self.client.post(
            path=reverse(
                "condo:condo_setup_apartment_delete",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            ),
            follow=True,
        )

        # verify redirect to success url
        expected_url = reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.block_one.pk},
        )
        self.assertRedirects(response, expected_url)

        # verify success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            f"Apartment {current_apartment.number_or_name} has been successfully deleted from {current_apartment.block.number_or_name}.",
            str(messages[0]),
        )

        # verify apartment was really deleted
        self.assertFalse(
            Apartment.objects.filter(pk=self.apartment_one_o_one.pk).exists()
        )

    ######### SetupApartmentMultipleCreateView() #########
    def test_apartmentmultiplecreateview_raises_error_if_condominium_doesnot_exist(
        self,
    ):
        # delete all condominiums from db
        Condominium.objects.all().delete()

        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.block_one.pk},
        )

        form_data = {
            "first_floor": 1,
            "last_floor": 2,
            "apartments_per_floor": 2,
        }
        # make a request
        response = self.client.post(url, form_data, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "In order to create apartments, you must create a condominium first.",
        )

    def test_apartmentmultiplecreateview_raises_error_if_block_doesnot_exist(self):
        # create a valid but inexistent random block_id
        block_id = uuid.uuid4()
        url = reverse(
            "condo:condo_setup_apartment_multiple_create", kwargs={"block_id": block_id}
        )
        form_data = {
            "first_floor": 1,
            "last_floor": 2,
            "apartments_per_floor": 2,
        }
        # make request
        response = self.client.post(url, form_data)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            "You are trying to create apartments in a block that does not exist",
        )

    def test_apartmentmultiplecreateview_render_correct_get_template(self):
        response = self.client.get(
            path=reverse(
                "condo:condo_setup_apartment_multiple_create",
                kwargs={"block_id": self.block_one.pk},
            )
        )
        self.assertTemplateUsed(
            response,
            "condo/pages/setup_pages/apartment/condo_setup_apartments_create_multiple.html",
        )
        # verify context
        self.assertEqual(response.context["current_block"], self.block_one)

    def test_apartmentmultiplecreateview_processes_initial_form_on_post_method(self):
        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.block_one.pk},
        )
        form_data = {
            "first_floor": 1,
            "last_floor": 2,
            "apartments_per_floor": 2,
        }
        # make request
        response = self.client.post(url, form_data)

        # verify is confirmation template is rendered
        self.assertTemplateUsed(
            response,
            "condo/pages/setup_pages/apartment/condo_setup_apartments_confirm_create_multiple.html",
        )
        # verify context
        self.assertEqual(response.context["current_block"], self.block_one)

    def test_apartmentmultiplecreate_bulk_creates_with_second_post_request(
        self,
    ):
        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.block_one.pk},
        )
        form_data = {
            "first_floor": 1,
            "last_floor": 2,
            "apartments_per_floor": 2,
        }
        # make initial request that prepares the data through first form
        self.client.post(url, form_data)

        # make second POST request with "confirm" parameter to start bulk creation
        second_response = self.client.post(
            url, data={"Confirm": "Confirm"}, follow=True
        )

        # verify redirect after apartments confirmation
        expected_url = reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.block_one.pk},
        )
        self.assertRedirects(second_response, expected_url)

        # verify success message
        messages = list(get_messages(second_response.wsgi_request))
        self.assertIn("have been created", str(messages[0]))

        # verify session data is deleted
        self.assertNotIn("apartments_to_create", self.client.session)

        # verify created apartment number_or_name
        created_apartments = Apartment.objects.filter(
            condominium=self.current_condominium, block=self.block_one
        ).order_by("number_or_name")
        apt_numbers = [apt.number_or_name for apt in created_apartments]
        self.assertEqual(set(apt_numbers), {"11", "12", "21", "22", "101"})

    def test_apartmentmultiplecreate_raises_error_if_duplicated_apartment(self):
        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.block_one.pk},
        )
        form_data = {
            "first_floor": 10,  # apartment 101 already exists in db!
            "last_floor": 11,
            "apartments_per_floor": 2,
        }

        # make requests (first to form, second to confirm)
        self.client.post(url, form_data)
        second_response = self.client.post(url, data={"Confirm": "Confirm"})

        # verify error message
        messages = list(get_messages(second_response.wsgi_request))
        self.assertIn(
            "The whole operation was canceled because the following apartments already exist",
            str(messages[0]),
        )
        # verify redirect is correct
        self.assertRedirects(
            second_response,
            reverse(
                "condo:condo_setup_apartment_multiple_create",
                kwargs={"block_id": self.block_one.pk},
            ),
        )

    def test_apartmentmultiplecreate_raises_error_if_session_doesnt_exist(self):
        url = reverse(
            "condo:condo_setup_apartment_multiple_create",
            kwargs={"block_id": self.block_one.pk},
        )
        form_data = {
            "first_floor": 1,
            "last_floor": 2,
            "apartments_per_floor": 2,
        }

        # make request to form
        self.client.post(url, form_data)

        # create a new client in order to be sure session data does not exist
        new_client = Client()
        new_client.login(username="johndoe", password="P@ssw0rd")

        # new_client makes a request to confirm (submit form)
        second_response = new_client.post(url, {"Confirm": "Confirm"})

        # No session data. Verify error message
        messages = list(get_messages(second_response.wsgi_request))
        self.assertEqual(
            "Please, fill in the blanks in order to create multiple apartments",
            str(messages[0]),
        )

        # verify correct redirect
        self.assertRedirects(
            second_response,
            reverse(
                "condo:condo_setup_apartment_multiple_create",
                kwargs={"block_id": self.block_one.pk},
            ),
        )

    ######### SetupApartmentEditView() #########
    def test_apartmenteditview_raises_dispatch_error_if_queryset_doesnot_exist(self):
        fake_id = uuid.uuid4()

        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_edit", kwargs={"apartment_id": fake_id}
            )
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            "The apartment you are trying to edit does not exist or "
            "you do not have permissions to do so.",
        )

        self.assertRedirects(
            response, reverse("condo:condo_setup_blocks_to_apartments")
        )

    def test_apartmenteditview_get_queryset_returns_correct_queryset(self):
        # access edit page that render edit form
        response = self.client.get(
            reverse(
                "condo:condo_setup_apartment_edit",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            )
        )
        # access the form from the context
        queryset = response.context["form"]

        self.assertEqual(queryset.instance, self.apartment_one_o_one)

    def test_apartmenteditview_get_context_data_returns_correct_context(self):
        response = self.client.get(
            reverse(
                "condo:condo_setup_apartment_edit",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            )
        )
        self.assertEqual(response.context["block_id"], self.block_one.pk)

    def test_apartmenteditview_raises_error_if_duplicated_number_or_name(self):
        # create second apartment
        Apartment.objects.create(
            condominium=self.current_condominium,
            block=self.block_one,
            number_or_name="202",
        )

        # send a request in order to try to change 101 to 202 (that already exists as
        # above)
        form_data = {"number_or_name": "202"}
        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_edit",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            ),
            data=form_data,
        )

        self.assertIn(
            "Apartment number (or name) already exists in this block. "
            "Please, choose a different one.",
            str(response.context["form"].errors.get("number_or_name")),
        )

    def test_apartmenteditview_raises_success_message_and_redirects_correctly(self):
        form_data = {"number_or_name": "202"}
        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_edit",
                kwargs={"apartment_id": self.apartment_one_o_one.pk},
            ),
            data=form_data,
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), "Apartment has been updated successfully.")

        self.assertRedirects(
            response,
            reverse(
                "condo:condo_setup_apartment_list_by_block",
                kwargs={"block_id": self.block_one.pk},
            ),
        )

    ######### SetupApartmentDeleteView() #########
    def test_apartmentdeleteview_raises_error_if_user_unauthorized_or_apto_doesnt_exist(
        self,
    ):
        # supose apartment does not exist
        fake_id = uuid.uuid4()

        # make a request with fake apartment uuid
        response = self.client.post(
            reverse(
                "condo:condo_setup_apartment_delete",
                kwargs={"apartment_id": fake_id},
            ),
            follow=True,
        )
        # verify if status code is 404
        self.assertEqual(response.status_code, 404)

        # verify if error message is rendered
        messages_list = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages_list[0]),
            "The apartment you're trying to delete either doesn't exist or you don't have permission to delete it.",
        )

        # supose apartment exists, but user does not belong to current condominium
        Condominium.objects.all().delete()

        response2 = self.client.post(
            reverse(
                "condo:condo_setup_apartment_delete",
                kwargs={"apartment_id": self.apartment_one_o_one.id},
            ),
            follow=True,
        )

        # verify if status code is 404
        self.assertEqual(response2.status_code, 404)

        # verify if error message is rendered

        messages_list_2 = list(get_messages(response2.wsgi_request))
        self.assertEqual(
            str(messages_list_2[0]),
            "The apartment you're trying to delete either doesn't exist or you don't have permission to delete it.",
        )
