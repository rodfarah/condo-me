"""
Testing SETUP BLOCK VIEWS
"""

import uuid

from apps.condo.models import Block, Condominium
from django.contrib.messages import get_messages
from django.urls import reverse

from .base_test_case import BaseTestCase


class SetupBlockViewsTest(BaseTestCase):
    """
    Tests all Block views. Notice there is one specific view for each CRUD item.
    """

    def setUp(self) -> None:
        """Create one block to current condominium"""
        super().setUp()
        block_one_data = {
            "number_or_name": "Block One",
            "description": "First Block",
        }

        url = reverse("condo:condo_setup_block_create")

        self.response = self.client.post(url, block_one_data, follow=True)

    ######### SetupBlockCreateView() #########

    def test_setupblockcreateview_creates_block(self):
        self.assertEqual(self.response.status_code, 200)

        messages = list(get_messages(self.response.wsgi_request))
        self.assertEqual(str(messages[0]), "Block has been created successfully.")

    def test_setupblockcreateview_sends_error_message_if_user_creates_block_with_no_condominium(
        self,
    ):
        Condominium.objects.all().delete()
        block_data = {
            "number_or_name": "Block with no Condo",
            "description": "Impossible to create",
        }
        url = reverse("condo:condo_setup_block_create")
        response = self.client.post(url, block_data, follow=True)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(messages)

        self.assertEqual(
            str(messages[0]),
            "In order to create a block, you must create a condominium first.",
        )

        self.assertRedirects(
            response,
            expected_url=reverse("condo:condo_setup_condominium"),
            status_code=302,
        )

    def test_setupblockcreateview_get_object_return_current_block_to_be_edited(self):
        # setUp already created one block
        block = Block.objects.first()

        # condo-setup/block/edit/<uuid:block_id>
        url = reverse("condo:condo_setup_block_edit", kwargs={"block_id": block.pk})
        # make a request
        response = self.client.get(url)
        self.assertEqual(response.context["block_id"], Block.objects.first().pk)

    def test_setupblockcreateview_add_error_to_form_if_duplicated_number_or_name(self):
        # create second block
        block_two_data = {
            "number_or_name": "Block One",  # duplicated name
            "description": "Second Block",
        }
        url = reverse("condo:condo_setup_block_create")
        response = self.client.post(url, block_two_data, follow=True)

        form = response.context["form"]
        # form should be invalid
        self.assertFalse(form.is_valid())
        # check if error was sent to form
        self.assertEqual(
            form.errors["number_or_name"][0],
            "Block number (or name) already exists in this condominium. Please, choose a different one.",
        )

    ######### SetupBlockEditView() #########

    def test_setupblockeditview_get_object_raises_error_when_invalid_uuid(self):
        # setUp already created one block, but let's create a random UUID
        block_id = uuid.uuid4()  # valid, but inexistent
        # condo-setup/block/edit/<uuid:block_id>
        url = reverse("condo:condo_setup_block_edit", kwargs={"block_id": block_id})
        # make a request
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "The block you are trying to edit does not exist, or you do not have\
                      permissions to do so.",
        )

    def test_setupblockeditview_add_error_to_form_if_new_number_or_name_already_exists(
        self,
    ):
        # create a second block that is unique
        second_block = Block.objects.create(
            condominium=self.current_condominium,
            number_or_name="Block Two",
            description="Second Block",
        )
        # edit second block name, same as first block
        second_block_form_data = {
            "number_or_name": "Block One",  # already exists
            "description": "same name as first block",
        }

        response = self.client.post(
            path=reverse(
                "condo:condo_setup_block_edit", kwargs={"block_id": second_block.id}
            ),
            data=second_block_form_data,
            follow=True,
        )

        self.assertEqual(
            response.context["form"].errors["number_or_name"][0],
            "Block number (or name) already exists in this condominium. Please, choose a different one.",
        )

    def test_setupblockeditview_saves_edited_block_and_raises_success_message(self):
        # edit test block
        edit_data = {
            "number_or_name": "Edited Block One",
            "description": "Editing Block One",
        }
        response = self.client.post(
            reverse(
                "condo:condo_setup_block_edit",
                kwargs={"block_id": Block.objects.get(number_or_name="Block One").pk},
            ),
            data=edit_data,
        )
        self.assertIn(
            response.content.decode("utf-8"), "Block has been updated successfully."
        )

    ######### SetupBlockListView() #########

    def test_setupblocklistview_sends_queryset(self):
        # create one more block
        Block.objects.create(
            number_or_name="Block Two",
            description="Second Block",
            condominium=self.current_condominium,
        )

        # get from block_list_view
        response = self.client.get(path=reverse("condo:condo_setup_block_list"))

        queryset = response.context["block_list"].order_by("id")

        # check if there are two objects inside queryset
        self.assertEqual(queryset.count(), 2)

        expected_blocks = Block.objects.all().order_by("id")
        self.assertQuerySetEqual(queryset, expected_blocks)


class SetupBlockDeleteViewTest(BaseTestCase):

    def setUp(self) -> None:
        """Create one block to current condominium"""
        super().setUp()
        block_one_data = {
            "number_or_name": "Block One",
            "description": "First Block",
        }

        url = reverse("condo:condo_setup_block_create")

        self.response = self.client.post(url, block_one_data, follow=True)

    def test_setupblockdeleteview_get_context_data_method(self):
        # get the only existing block, created by setUp
        current_block = Block.objects.first()

        # "condo-setup/block/delete/<uuid:block_id>/",
        url = reverse(
            "condo:condo_setup_block_delete", kwargs={"block_id": current_block.pk}
        )
        # make a request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["block"], current_block)

    def test_setupblockdeleteview_form_valid_succeeds(self):
        # get the only existing block, created by setUp
        current_block = Block.objects.first()

        url = reverse(
            "condo:condo_setup_block_delete", kwargs={"block_id": current_block.pk}
        )
        # make a request
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), "Block has been successfully deleted.")
