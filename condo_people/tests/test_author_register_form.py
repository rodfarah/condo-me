from django.test import TestCase

from condo_people.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    def test_first_name_placeholder_is_correct(self):
        """Tests if a placeholder is correctly rendered in the template"""
        form = RegisterForm()
        placeholder = form['first_name'].field.widget.attrs['placeholder']
        self.assertEqual('first name', placeholder)
