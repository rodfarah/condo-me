"""
'test_setup_condominium_views' are applied to the condominium configuration page,
accessible only to 'manager' users.
These tests are DIFFERENT from 'test_condo_views' which are applied to the first page user will get when logged in.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from apps.condo.models import Condominium


class CondoSetupViewsTest(TestCase):
    """Condo SetUp Views Tests. Please, consider condo views are login_required"""

    # setup for starting each test
    def setUp(self) -> None:
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
        manager_group, already_exists = Group.objects.get_or_create(name="manager")
        self.current_user.groups.add(manager_group)
        self.current_user.save()

        # login user
        self.client.login(username="johndoe", password="P@ssw0rd")

    ######################################
    ###### Testing SETUP AREA VIEWS ######
    ######################################

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


class SetupCondominiumViewsTest(CondoSetupViewsTest):
    def test_condo_exists_is_none_if_condominium_is_none(self):
        # remove setup condominium instance from db
        Condominium.objects.all().delete()
        # Create a get request
        url = reverse("condo:condo_setup_block_list")
        response = self.client.get(path=url)

        self.assertEqual(response.context["condo_exists"], False)
