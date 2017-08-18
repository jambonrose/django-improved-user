"""Test integration of Improved User with Django & Django Registration

The goal is to ensure that all views provided by registration work as
desired with improved user. These end-to-end tests may be used on full
sites.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from improved_user.forms import UserCreationForm

# TODO: remove the conditional import when Dj 1.10 dropped
try:
    from django.urls import reverse  # pylint: disable=ungrouped-imports
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse


class TestViews(TestCase):
    """Test Registration views to ensure User integration"""

    def test_account_registration(self):
        """Test that users can register Improved User accounts"""
        User = get_user_model()  # pylint: disable=invalid-name
        email = 'hello@jambonsw.com'
        password = 's4f3passw0rd!'
        get_response = self.client.get(reverse('registration_register'))
        self.assertEqual(200, get_response.status_code)
        self.assertIsInstance(get_response.context['form'], UserCreationForm)
        self.assertTemplateUsed('registration/registration_form.html')
        self.assertTemplateUsed('base.html')
        post_response = self.client.post(
            reverse('registration_register'),
            data={
                'email': email,
                'password1': password,
                'password2': password,
            },
        )
        self.assertRedirects(post_response, reverse('registration_complete'))
        self.assertTrue(
            User.objects.filter(email=email).exists())
        user = User.objects.get(email=email)
        self.assertTrue(user.check_password(password))
