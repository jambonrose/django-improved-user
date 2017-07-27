from __future__ import unicode_literals

from unittest import skipUnless

import django
from django.forms import Field
from django.test import TestCase, override_settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from ..forms import UserChangeForm, UserCreationForm
from ..models import User


@override_settings(
    USE_TZ=False,
    PASSWORD_HASHERS=('django.contrib.auth.hashers.SHA1PasswordHasher',),
)
class UserCreationFormTest(TestCase):

    fixtures = ['authtestdata.json']

    def test_user_already_exists(self):
        data = {
            'email': 'testclient@example.com',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["email"].errors,
                         [force_text(form.error_messages['duplicate_email'])])

    def test_invalid_data(self):
        data = {
            'email': 'jsmith!',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["email"].errors, [_('Enter a valid email address.')])

    def test_password_verification(self):
        # The verification password is incorrect.
        data = {
            'email': 'jsmith@example.com',
            'password1': 'test123',
            'password2': 'test',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["password2"].errors,
                         [force_text(form.error_messages['password_mismatch'])])

    def test_both_passwords(self):
        # One (or both) passwords weren't given
        data = {'email': 'jsmith@example.com'}
        form = UserCreationForm(data)
        required_error = [force_text(Field.default_error_messages['required'])]
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, required_error)

        data['password2'] = 'test123'
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, [])

    def test_success(self):
        # The success case.
        data = {
            'email': 'jsmith@example.com',
            'full_name': 'John Smith',
            'short_name': 'John',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        u = form.save()
        self.assertEqual(repr(u), '<User: jsmith@example.com>')

    @skipUnless(django.VERSION >= (1, 9), "Password strength checks not available on Django 1.8")
    @override_settings(
        AUTH_PASSWORD_VALIDATORS = [
            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        ]
    )
    def test_common_password(self):
        data = {
            'email': 'jsmith@example.com',
            'password1': 'password',
            'password2': 'password',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["password1"].errors, ['This password is too common.'])

    @skipUnless(django.VERSION >= (1, 9), "Password strength checks not available on Django 1.8")
    @override_settings(
        AUTH_PASSWORD_VALIDATORS = [{
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            'OPTIONS': { 'user_attributes': ('email', 'full_name', 'short_name') },
        }]
    )
    def test_password_help_text(self):
        form = UserCreationForm()
        self.assertEqual(
            form.fields['password1'].help_text,
            '<ul><li>Your password can&#39;t be too similar to'
            ' your other personal information.</li></ul>')

    @skipUnless(django.VERSION >= (1, 9), "Password strength checks not available on Django 1.8")
    @override_settings(
        AUTH_PASSWORD_VALIDATORS = [{
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            'OPTIONS': { 'user_attributes': ('email', 'full_name', 'short_name') },
        }]
    )
    def test_similar_attribute(self):
        data = {
            'email': 'jsmith@example.com',
            'password1': 'johndoesmith',
            'password2': 'johndoesmith',
            'full_name': 'John Doe Smith',
            'short_name': 'John',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form["password1"].errors,
            ['The password is too similar to the full name.'])


@override_settings(
    USE_TZ=False,
    PASSWORD_HASHERS=('django.contrib.auth.hashers.SHA1PasswordHasher',)
)
class UserChangeFormTest(TestCase):

    fixtures = ['authtestdata.json']

    def test_email_validity(self):
        user = User.objects.get(email='testclient@example.com')
        data = {'email': 'not valid'}
        form = UserChangeForm(data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["email"].errors, [_('Enter a valid email address.')])

    def test_bug_14242(self):
        # A regression test, introduce by adding an optimization for the
        # UserChangeForm.

        class MyUserForm(UserChangeForm):
            def __init__(self, *args, **kwargs):
                super(MyUserForm, self).__init__(*args, **kwargs)
                self.fields['groups'].help_text = 'These groups give users different permissions'

            class Meta(UserChangeForm.Meta):
                fields = ('groups',)

        # Just check we can create it
        MyUserForm({})

    def test_unusable_password(self):
        user = User.objects.get(email='empty_password@example.com')
        user.set_unusable_password()
        user.save()
        form = UserChangeForm(instance=user)
        self.assertIn(_("No password set."), form.as_table())

    def test_bug_17944_empty_password(self):
        user = User.objects.get(email='empty_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(_("No password set."), form.as_table())

    def test_bug_17944_unmanageable_password(self):
        user = User.objects.get(email='unmanageable_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(_("Invalid password format or unknown hashing algorithm."),
            form.as_table())

    def test_bug_17944_unknown_password_algorithm(self):
        user = User.objects.get(email='unknown_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(_("Invalid password format or unknown hashing algorithm."),
            form.as_table())

    def test_bug_19133(self):
        "The change form does not return the password value"
        # Use the form to construct the POST data
        user = User.objects.get(email='testclient@example.com')
        form_for_data = UserChangeForm(instance=user)
        post_data = form_for_data.initial

        # The password field should be readonly, so anything
        # posted here should be ignored; the form will be
        # valid, and give back the 'initial' value for the
        # password field.
        post_data['password'] = 'new password'
        form = UserChangeForm(instance=user, data=post_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], 'sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161')

    def test_bug_19349_bound_password_field(self):
        user = User.objects.get(email='testclient@example.com')
        form = UserChangeForm(data={}, instance=user)
        # When rendering the bound password field,
        # ReadOnlyPasswordHashWidget needs the initial
        # value to render correctly
        self.assertEqual(form.initial['password'], form['password'].value())
