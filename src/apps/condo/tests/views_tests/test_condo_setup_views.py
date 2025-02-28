"""
'test_setup_condominium_views' are applied to the condominium configuration page,
accessible only to 'manager' users.
These tests are DIFFERENT from 'test_condo_base_views' which are applied to the first page 
user will get when logged in.
"""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.condo.models import Apartment, Block, Condominium


class BaseTestCase(TestCase):
    """This class has all commmon setup for all tests"""

    def setUp(self) -> None:
        """
        Set up the test environment for the condo setup views tests.
        This method performs the following actions:
        1. Calls the parent class's setUp method.
        2. Creates a user with the specified details.
        3. Creates a condominium with the specified details.
        4. Assigns the created condominium to the created user.
        5. Adds the created user to the "manager" group.
        6. Logs in the created user.
        Attributes:
            current_user (User): The user created for testing.
            current_condominium (Condominium): The condominium created for testing.
        """
        super().setUp()
        # create user
        self.current_user = get_user_model().objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@dummy.com",
            username="johndoe",
            password="P@ssw0rd",
        )

        # create condominium
        self.current_condominium = Condominium.objects.create(
            name="MyCondo",
            description="Good Condo",
            cnpj="15306944000169",
            address1="My Street, 10",
            address2="Wonderland",
            city="Soma City",
            state="Wellness State",
            country="BR",
            postal_code="88456123",
        )
        # assign condominium to user
        self.current_user.condominium = self.current_condominium

        # make user belong to "manager" group
        manager_group, bool_already_exists = Group.objects.get_or_create(name="manager")
        self.current_user.groups.add(manager_group)
        self.current_user.save()

        # login user
        self.client.login(username="johndoe", password="P@ssw0rd")


######################################
###### Testing SETUP AREA VIEWS ######
######################################


class SetupAreaViewsTest(BaseTestCase):
    def test_manager_group_required_permission_denied(self):
        # get user in db
        current_user = get_user_model().objects.first()
        # create a "test user group" and assign it to current user
        test_user_group = Group.objects.create(name="test_user_group")
        current_user.groups.add(test_user_group)
        # remove "manager" group from setup
        manager_group = Group.objects.get(name="manager")
        current_user.groups.remove(manager_group.pk)
        current_user.save()
        # user tries to access setup pages
        response = self.client.get(reverse("condo:condo_setup_home"))
        self.assertEqual(response.status_code, 403)

    def test_manager_user_with_condo_gets_setup_basic_page_rendered_successfully(self):
        response = self.client.get(reverse("condo:condo_setup_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "condo/pages/setup_pages/setup_main/condo_setup_home.html"
        )

    def test_user_doesnt_have_condo_gets_rendered_template_without_context(self):
        # remove condominium from user
        self.current_user.condominium = None
        self.current_user.save()
        # create a request
        response = self.client.get(reverse("condo:condo_setup_home"))
        self.assertNotIn("condo_page", response.context)


#############################################
###### Testing SETUP CONDOMINIUM VIEWS ######
#############################################


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


#############################################
######### Testing SETUP Block VIEWS #########
#############################################


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
                      permitions to do so.",
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


#################################################
######### Testing SETUP Apartment VIEWS #########
#################################################


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
        self.assertTrue(
            Apartment.objects.filter(
                number_or_name="101",
                block=self.block_one,
                condominium=self.current_condominium,
            ).exists()
        )
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
        self.assertIn("Apartment has been successfully deleted", str(messages[0]))

        # verify apartment was really deleted
        self.assertFalse(
            Apartment.objects.filter(pk=self.apartment_one_o_one.pk).exists()
        )
