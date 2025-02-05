"""
'test_setup_condominium_views' are applied to the condominium configuration page,
accessible only to 'manager' users.
These tests are DIFFERENT from 'test_condo_views' which are applied to the first page user will get when logged in.
"""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.condo.models import Block, Condominium


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
            response, "condo/pages/setup_pages/condo_setup_home.html"
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


class SetupBlockViewTest(BaseTestCase):
    def setUp(self) -> None:
        """Create one block to current condominium"""
        super().setUp()
        block_one_data = {
            "name": "Block One",
            "description": "First Block",
            "condominium": self.current_condominium,
        }

        url = reverse("condo:condo_setup_block_create")

        self.response = self.client.post(url, block_one_data, follow=True)

    def test_setupblockview_creates_block(self):
        self.assertEqual(self.response.status_code, 200)

        messages = list(get_messages(self.response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Block has been created or edited successfully"
        )

    def test_setupblockview_sends_error_message_if_user_creates_block_with_no_condominium(
        self,
    ):
        Condominium.objects.all().delete()
        block_data = {
            "name": "Block with no Condo",
            "description": "Impossible to create",
        }
        url = reverse("condo:condo_setup_block_create")
        response = self.client.post(url, block_data, follow=True)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(messages)

        self.assertEqual(
            str(messages[0]),
            "In order to create or edit a block, you must create a condominium first.",
        )

        self.assertRedirects(
            response,
            expected_url=reverse("condo:condo_setup_condominium"),
            status_code=302,
        )

    def test_setupblockview_get_queryset(self):
        # make a request
        response = self.client.get(reverse("condo:condo_setup_block_create"))
        # test view behavior
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "condo/pages/setup_pages/condo_setup_block.html"
        )
        # verify queryset through context
        self.assertIn(Block.objects.first(), response.context["object_list"])

    def test_setupblockview_get_object_return_current_block_to_be_edited(self):
        # setUp already created one block
        block = Block.objects.first()

        # condo-setup/block/edit/<uuid:block_id>
        url = reverse("condo:condo_setup_block_edit", kwargs={"block_id": block.pk})
        # make a request
        response = self.client.get(url)
        self.assertEqual(response.context["block_id"], Block.objects.first().pk)

    def test_setupblockview_get_object_raises_error_when_invalid_uuid(self):
        # setUp already created one block, but let's create a random UUID
        block_id = uuid.uuid4()  # valid, but inexistent
        # condo-setup/block/edit/<uuid:block_id>
        url = reverse("condo:condo_setup_block_edit", kwargs={"block_id": block_id})
        # make a request
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "This block does not exist or you do not have permission to edit it",
        )


class SetupBlockListViewTest(BaseTestCase):
    def setUp(self) -> None:
        """Create one block to current condominium"""
        super().setUp()
        block_one_data = {
            "name": "Block One",
            "description": "First Block",
            "condominium": self.current_condominium,
        }

        url = reverse("condo:condo_setup_block_create")

        self.response = self.client.post(url, block_one_data, follow=True)

    def test_view_sends_queryset(self):
        # create one more block
        Block.objects.create(
            name="Block Two",
            description="Second Block",
            condominium=self.current_condominium,
        )

        # get from block_list_view
        response = self.client.get(path=reverse("condo:condo_setup_block_list"))

        queryset = response.context["object_list"].order_by("id")

        # check if there are two objects inside queryset
        self.assertEqual(queryset.count(), 2)

        expected_blocks = Block.objects.all().order_by("id")
        self.assertQuerySetEqual(queryset, expected_blocks)
