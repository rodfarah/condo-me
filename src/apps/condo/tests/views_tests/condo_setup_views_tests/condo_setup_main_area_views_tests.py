"""
Testing SETUP MAIN AREA VIEWS
The first page rendered when user gets inside "Condominium Setup"
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from .base_test_case import BaseTestCase


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
