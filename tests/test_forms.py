"""Test UserCreationForm and UserChangeForm"""
from unittest import skipUnless
from unittest.mock import patch

from django import VERSION as DjangoVersion
from django.forms.fields import Field
from django.test import TestCase, override_settings
from django.utils.translation import gettext as _

from improved_user.forms import UserChangeForm, UserCreationForm
from improved_user.models import User


class TestDataMixin:  # pylint: disable=too-few-public-methods
    """Mixin used by both test classes below; creates users"""

    @classmethod
    def setUpTestData(cls):
        """Called by TestCase during initialization; creates users"""
        cls.u1 = User.objects.create_user(
            email='testclient@example.com',
            password='password',
            short_name='tester')
        cls.u2 = User.objects.create_user(
            email='inactive@example.com',
            password='password',
            is_active=False)
        cls.u3 = User.objects.create_user(
            email='staff@example.com',
            password='password')
        cls.u4 = User.objects.create(
            email='empty_password@example.com',
            password='')
        cls.u5 = User.objects.create(
            email='unmanageable_password@example.com',
            password='$')
        cls.u6 = User.objects.create(
            email='unknown_password@example.com',
            password='foo$bar')


class UserCreationFormTest(TestDataMixin, TestCase):
    """Test UserCreationForm with Improved User"""

    def test_user_already_exists(self):
        """Raise errors if user already exists"""
        data = {
            'email': 'testclient@example.com',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors,
                         [str(form.error_messages['duplicate_email'])])

    def test_invalid_data(self):
        """Raise errors if invalid email format"""
        data = {
            'email': '%%%',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        validator = next(v
                         for v in User._meta.get_field('email').validators
                         if v.code == 'invalid')
        self.assertEqual(form['email'].errors, [str(validator.message)])

    def test_password_verification(self):
        """The verification password is incorrect."""
        data = {
            'email': 'jsmith@example.com',
            'password1': 'test123',
            'password2': 'test',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors,
                         [str(form.error_messages['password_mismatch'])])

    def test_both_passwords(self):
        """One (or both) passwords weren't given"""
        data = {'email': 'jsmith@example.com'}
        form = UserCreationForm(data)
        required_error = [str(Field.default_error_messages['required'])]
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, required_error)

        data['password2'] = 'test123'
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, [])

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    @patch('django.contrib.auth.password_validation.password_changed')
    def test_success(self, password_changed):
        """Successful submission of form data"""
        data = {
            'email': 'jsmith@example.com',
            'full_name': 'John Smith',  # optional field
            'short_name': 'John',  # optional field
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(password_changed.call_count, 0)
        user = form.save()
        self.assertEqual(password_changed.call_count, 1)
        self.assertEqual(repr(user), '<User: jsmith@example.com>')
        self.assertEqual(user.get_short_name(), 'John')
        self.assertEqual(user.get_full_name(), 'John Smith')
        self.assertTrue(user.check_password('test123'))

    # TODO: Remove this test in favor of above after Dj1.8 dropped
    @skipUnless(
        DjangoVersion < (1, 9),
        'Password strength checks not available on Django 1.8')
    def test_success_pre_19(self):
        """Successful submission of form data"""
        data = {
            'email': 'jsmith@example.com',
            'full_name': 'John Smith',  # optional field
            'short_name': 'John',  # optional field
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(repr(user), '<User: jsmith@example.com>')
        self.assertEqual(user.get_short_name(), 'John')
        self.assertEqual(user.get_full_name(), 'John Smith')
        self.assertTrue(user.check_password('test123'))

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    @override_settings(
        AUTH_PASSWORD_VALIDATORS=[
            {'NAME': 'django.contrib.auth.password_validation.'
                     'CommonPasswordValidator'},
            {'NAME': 'django.contrib.auth.password_validation.'
                     'MinimumLengthValidator',
             'OPTIONS': {'min_length': 12}}])
    def test_common_password(self):
        """Ensure form works with Password Validation"""
        data = {
            'email': 'jsmith@example.com',
            'password1': 'password',
            'password2': 'password',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form['password1'].errors), 2)
        self.assertIn(
            'This password is too common.',
            form['password1'].errors)
        self.assertIn(
            'This password is too short. '
            'It must contain at least 12 characters.',
            form['password1'].errors)

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    @override_settings(
        AUTH_PASSWORD_VALIDATORS=[
            {'NAME': 'django.contrib.auth.password_validation.'
                     'UserAttributeSimilarityValidator'}])
    def test_validates_password_similarity_length(self):
        """Test misconfigured-similarity validator catches email"""
        data = {
            'email': 'jsmith@example.com',
            'password1': 'jsmith',
            'password2': 'jsmith',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'The password is too similar to the email address.',
            form['password1'].errors)

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    @override_settings(
        AUTH_PASSWORD_VALIDATORS=[{
            'NAME': 'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator',
            'OPTIONS': {
                'user_attributes': ('email', 'full_name', 'short_name')}}])
    def test_password_help_text(self):
        """Ensure UserAttributeSimilarityValidator help text is shown"""
        form = UserCreationForm()
        self.assertEqual(
            form.fields['password1'].help_text,
            '<ul><li>Your password can&#39;t be too similar to'
            ' your other personal information.</li></ul>')

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    @override_settings(
        AUTH_PASSWORD_VALIDATORS=[{
            'NAME': 'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator',
            'OPTIONS': {
                'user_attributes': ('email', 'full_name', 'short_name')}}])
    def test_validates_password_with_all_data(self):
        """Test correctly configured similarity validatior catches name"""
        data = {
            'email': 'jsmith@example.com',
            'password1': 'johndoesmith',
            'password2': 'johndoesmith',
            'short_name': 'John',
            'full_name': 'John Smith',
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password1'].errors,
            ['The password is too similar to the full name.'])

    def test_password_whitespace_not_stripped(self):
        """Ensure we aren't mangling passwords by removing whitespaces

        Starting in Django 1.9, form Charfield and subclasses allow for
        whitestrip to be stripped automatically during the clean field
        phase. This is a test to ensure that we are not stripping
        whitespace from the password.

        """
        data = {
            'email': 'jsmith@example.com',
            'password1': '   test password   ',
            'password2': '   test password   ',
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password1'], data['password1'])
        self.assertEqual(form.cleaned_data['password2'], data['password2'])


class UserChangeFormTest(TestDataMixin, TestCase):
    """Tests for UserChangeForm"""

    def test_email_validity(self):
        """Ensure Email Validation is used on User"""
        user = User.objects.get(email='testclient@example.com')
        data = {'email': 'not valid'}
        form = UserChangeForm(data, instance=user)
        self.assertFalse(form.is_valid())
        validator = next(v
                         for v in User._meta.get_field('email').validators
                         if v.code == 'invalid')
        self.assertEqual(form['email'].errors, [str(validator.message)])

    def test_bug_14242(self):
        """Regression test: allow UserChangeForm subclasses

        https://code.djangoproject.com/ticket/14242

        """
        class MyUserForm(UserChangeForm):
            """Custom Subclass to check lack of user_permissions field"""
            def __init__(self, *args, **kwargs):
                super(MyUserForm, self).__init__(*args, **kwargs)
                self.fields['groups'].help_text = (
                    'These groups give users different permissions')

            class Meta(UserChangeForm.Meta):
                fields = ('groups',)

        # Just check we can create it
        MyUserForm({})

    def test_unusable_password(self):
        """Test that Django shows unusable password warning"""
        user = User.objects.get(email='empty_password@example.com')
        user.set_unusable_password()
        user.save()
        form = UserChangeForm(instance=user)
        self.assertIn(_('No password set.'), form.as_table())

    def test_bug_17944_empty_password(self):
        """Test form can be used when password not set

        https://code.djangoproject.com/ticket/17944

        """
        user = User.objects.get(email='empty_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(_('No password set.'), form.as_table())

    def test_bug_17944_unmanageable_password(self):
        """Test form can be used when password unmanageable

        https://code.djangoproject.com/ticket/17944

        """
        user = User.objects.get(email='unmanageable_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(
            _('Invalid password format or unknown hashing algorithm.'),
            form.as_table())

    def test_bug_17944_unknown_password_algorithm(self):
        """Test form can be used when hashing algorithm is unrecognized

        https://code.djangoproject.com/ticket/17944

        """
        user = User.objects.get(email='unknown_password@example.com')
        form = UserChangeForm(instance=user)
        self.assertIn(
            _('Invalid password format or unknown hashing algorithm.'),
            form.as_table())

    def test_bug_19133(self):
        """The change form does not return the password value

        https://code.djangoproject.com/ticket/19133

        """
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
        self.assertTrue(user.check_password('password'))  # $ not in password
        self.assertIn('$', form.cleaned_data['password'])  # hash contains $

    def test_bug_19349_bound_password_field(self):
        """Test re-rendering of ReadOnlyPasswordHashWidget

        https://code.djangoproject.com/ticket/19349

        """
        user = User.objects.get(email='testclient@example.com')
        form = UserChangeForm(data={}, instance=user)
        # When rendering the bound password field,
        # ReadOnlyPasswordHashWidget needs the initial
        # value to render correctly
        self.assertEqual(form.initial['password'], form['password'].value())
