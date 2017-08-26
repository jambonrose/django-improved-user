"""Test integration of Improved User with Django & Django Registration

The goal is to ensure that all views provided by registration work as
desired with improved user. These end-to-end tests may be used on full
sites.
"""
from re import search as re_search

from django import VERSION as DjangoVersion
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from improved_user.forms import UserCreationForm

# TODO: remove the conditional import when Dj 1.10 dropped
try:
    from django.urls import reverse  # pylint: disable=ungrouped-imports
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse


class TestDataMigration(TestCase):
    """Test that the Improved User may be used in data migrations"""

    def test_user_exists(self):
        """Check UserManager properly created user"""
        User = get_user_model()  # pylint: disable=invalid-name
        self.assertTrue(
            User.objects.filter(email='migrated@jambonsw.com').exists())


class TestViews(TestCase):
    """Test Registration views to ensure User integration"""

    def test_home(self):
        """Test that homeview returns basic template"""
        get_response = self.client.get(reverse('home'))
        self.assertEqual(200, get_response.status_code)
        self.assertTemplateUsed(get_response, 'home.html')
        self.assertTemplateUsed(get_response, 'base.html')

    def test_tester(self):
        """Ensure that tests behave as expected"""
        email = 'hello@jambonsw.com'
        password = 's4f3passw0rd!'
        User = get_user_model()  # pylint: disable=invalid-name
        User.objects.create_user(email, password)
        self.assertTrue(self.client.login(username=email, password=password))

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
        self.assertFalse(user.is_active)
        self.assertFalse(self.client.login(username=email, password=password))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertEqual(
            mail.outbox[0].subject, 'Account activation on testserver')
        urlmatch = re_search(
            r'https?://[^/]*(/.*activate/\S*)',
            mail.outbox[0].body)
        self.assertIsNotNone(urlmatch, 'No URL found in sent email')
        url_path = urlmatch.groups()[0]
        self.assertEqual(
            reverse('registration_activate',
                    kwargs={'activation_key': url_path.split('/')[3]}),
            url_path)
        activation_get_response = self.client.get(url_path)
        self.assertRedirects(
            activation_get_response,
            reverse('registration_activation_complete'))
        # reload user from DB
        user = User.objects.get(email=email)
        self.assertTrue(user.is_active)
        self.assertTrue(self.client.login(username=email, password=password))

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
        # TODO: remove condition when Dj 1.8 dropped
        if DjangoVersion >= (1, 10):
            self.assertRedirects(get_logout_response, reverse('auth_login'))

    def test_password_change(self):
        """Simulate a user changing their password"""
        email = 'hello@jambonsw.com'
        password = 's4f3passw0rd!'
        newpassword = 'neo.h1m1tsu!'
        User = get_user_model()  # pylint: disable=invalid-name
        User.objects.create_user(email, password)

        response = self.client.get(reverse('auth_password_change'))
        self.assertRedirects(
            response,
            '{}?next={}'.format(
                reverse(settings.LOGIN_URL), reverse('auth_password_change')))
        self.client.login(username=email, password=password)
        response = self.client.get(reverse('auth_password_change'))
        # WARNING:
        # this uses Django's admin template
        # to change this behavior, place user_integration app before
        # the admin app in the INSTALLED_APPS settings
        self.assertTemplateUsed(
            response, 'registration/password_change_form.html')

        data = {
            'old_password': password,
            'new_password1': newpassword,
            'new_password2': newpassword,
        }
        response = self.client.post(
            reverse('auth_password_change'), data=data, follow=True)
        self.assertRedirects(response, reverse('auth_password_change_done'))
        self.assertEqual(response.status_code, 200)
        # WARNING:
        # this uses Django's admin template
        # to change this behavior, place user_integration app before
        # the admin app in the INSTALLED_APPS settings
        self.assertTemplateUsed(
            response, 'registration/password_change_done.html')

        self.client.logout()
        self.assertTrue(
            self.client.login(username=email, password=newpassword))

    def test_password_reset(self):
        """Simulate a user resetting their password"""
        email = 'hello@jambonsw.com'
        password = 's4f3passw0rd!'
        newpassword = 'neo.h1m1tsu!'
        User = get_user_model()  # pylint: disable=invalid-name
        User.objects.create_user(email, password)

        response = self.client.get(reverse('auth_password_reset'))
        self.assertEqual(response.status_code, 200)
        # WARNING:
        # this uses Django's admin template
        # to change this behavior, place user_integration app before
        # the admin app in the INSTALLED_APPS settings
        self.assertTemplateUsed(
            response, 'registration/password_reset_form.html')

        data = {'email': email}
        post_response = self.client.post(
            reverse('auth_password_reset'),
            data=data,
            follow=True)
        self.assertRedirects(
            post_response, reverse('auth_password_reset_done'))
        # WARNING:
        # this uses Django's admin template
        # to change this behavior, place user_integration app before
        # the admin app in the INSTALLED_APPS settings
        self.assertTemplateUsed(
            post_response, 'registration/password_reset_done.html')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertEqual(
            mail.outbox[0].subject, 'Password reset on testserver')
        urlmatch = re_search(r'https?://[^/]*(/.*reset/\S*)',
                             mail.outbox[0].body)
        self.assertIsNotNone(urlmatch, 'No URL found in sent email')

        url_path = urlmatch.groups()[0]
        *_, uidb64, token = filter(None, url_path.split('/'))
        self.assertEqual(
            reverse('auth_password_reset_confirm',
                    kwargs={'uidb64': uidb64, 'token': token}),
            url_path)
        reset_get_response = self.client.get(url_path)
        self.assertEqual(reset_get_response.status_code, 200)
        # WARNING:
        # this uses Django's admin template
        # to change this behavior, place user_integration app before
        # the admin app in the INSTALLED_APPS settings
        self.assertTemplateUsed(
            reset_get_response, 'registration/password_reset_confirm.html')

        data = {
            'new_password1': newpassword,
            'new_password2': newpassword,
        }
        reset_post_response = self.client.post(
            url_path, data=data, follow=True)
        self.assertRedirects(
            reset_post_response, reverse('auth_password_reset_complete'))

        self.assertTrue(
            self.client.login(username=email, password=newpassword))
