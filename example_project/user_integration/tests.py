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

    def test_home(self):
        get_response = self.client.get(reverse('home'))
        self.assertEqual(200, get_response.status_code)
        self.assertTemplateUsed(get_response, 'home.html')
        self.assertTemplateUsed(get_response, 'base.html')

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

    def test_user_login_logout(self):
        """Simulate a user logging in and then out"""
        email = 'hello@jambonsw.com'
        password = 's4f3passw0rd!'
        User = get_user_model()  # pylint: disable=invalid-name
        User.objects.create_user(email, password)
        self.assertTrue(User.objects.filter(email=email).exists())

        # get login
        get_response = self.client.get(reverse('auth_login'))
        self.assertEqual(200, get_response.status_code)
        self.assertTemplateUsed(get_response, 'registration/login.html')
        self.assertTemplateUsed(get_response, 'base.html')

        # post login
        form_data = {
            'username': email,
            'password': password,
        }
        post_response = self.client.post(reverse('auth_login'), data=form_data)
        self.assertRedirects(post_response, reverse('home'))

        # logout
        get_logout_response = self.client.get(reverse('auth_logout'))
        self.assertRedirects(get_logout_response, reverse('auth_login'))
