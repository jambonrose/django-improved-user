"""Test Admin interface provided by Improved User"""
import os
import re

from django import VERSION as DjangoVersion
from django.contrib.admin.models import LogEntry
from django.contrib.auth import SESSION_KEY
from django.test import TestCase, override_settings
from django.test.utils import patch_logger
from django.utils.encoding import force_text

from improved_user.admin import UserAdmin
from improved_user.forms import UserChangeForm, UserCreationForm
from improved_user.models import User

# TODO: remove conditional import when Dj 1.8 dropped
# pylint: disable=ungrouped-imports
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
# pylint: enable=ungrouped-imports


# Redirect in test_user_change_password will fail if session auth hash
# isn't updated after password change (#21649)
@override_settings(ROOT_URLCONF='tests.urls')
class UserAdminTests(TestCase):
    """Based off django.tests.auth_tests.test_views.ChangelistTests"""

    @classmethod
    def setUpTestData(cls):
        """Called by TestCase during initialization; creates users"""
        cls.user1 = User.objects.create_user(
            email='testclient@example.com',
            password='password',
        )
        cls.user2 = User.objects.create_user(
            email='staffmember@example.com',
            password='password',
        )

    def setUp(self):
        """Make user1 a superuser before logging in."""
        User.objects\
            .filter(email='testclient@example.com')\
            .update(is_staff=True, is_superuser=True)
        self.login()
        self.admin = User.objects.get(pk=self.user1.pk)

    def login(self, username='testclient@example.com', password='password'):
        """Helper function to login the user (specified or default)"""
        response = self.client.post('/login/', {
            'username': username,
            'password': password,
        })
        self.assertIn(SESSION_KEY, self.client.session)
        return response

    def logout(self):
        """Helper function to logout the user"""
        response = self.client.get('/admin/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def get_user_data(self, user):  # pylint: disable=no-self-use
        """Generate dictionary of values to compare against"""
        return {
            'email': user.email,
            'password': user.password,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'last_login_0': user.last_login.strftime('%Y-%m-%d'),
            'last_login_1': user.last_login.strftime('%H:%M:%S'),
            'initial-last_login_0': user.last_login.strftime('%Y-%m-%d'),
            'initial-last_login_1': user.last_login.strftime('%H:%M:%S'),
            'date_joined_0': user.date_joined.strftime('%Y-%m-%d'),
            'date_joined_1': user.date_joined.strftime('%H:%M:%S'),
            'initial-date_joined_0': user.date_joined.strftime('%Y-%m-%d'),
            'initial-date_joined_1': user.date_joined.strftime('%H:%M:%S'),
            'full_name': user.full_name,
            'short_name': user.short_name,
        }

    def test_display_fields(self):
        """Test that admin shows all user fields"""
        excluded_model_fields = ['id', 'logentry']
        model_fields = set(
            field.name for field in User._meta.get_fields()
            if field.name not in excluded_model_fields
        )
        admin_fieldset_fields = set(
            fieldname
            for name, fieldset in UserAdmin.fieldsets
            for fieldname in fieldset['fields']
        )
        self.assertEqual(model_fields, admin_fieldset_fields)

    def test_add_has_required_fields(self):
        """Test all required fields in Admin Add view"""
        excluded_model_fields = [
            'date_joined', 'is_active', 'is_staff', 'is_superuser', 'password',
        ]
        required_model_fields = [
            field.name
            for field in User._meta.get_fields()
            if (field.name not in excluded_model_fields
                and hasattr(field, 'null') and field.null is False
                and hasattr(field, 'blank') and field.blank is False)
        ]
        extra_form_fields = [
            field_name
            for field_name in list(
                UserCreationForm.declared_fields,  # pylint: disable=no-member
            )
        ]
        admin_add_fields = [
            fieldname
            for name, fieldset in UserAdmin.add_fieldsets
            for fieldname in fieldset['fields']
        ]
        for field in required_model_fields+extra_form_fields:
            with self.subTest(field=field):
                self.assertIn(field, admin_add_fields)

    def test_correct_forms_used(self):
        """Test that UserAdmin uses the right forms"""
        self.assertIs(UserAdmin.add_form, UserCreationForm)
        self.assertIs(UserAdmin.form, UserChangeForm)

    def test_user_add(self):
        """Ensure the admin add view works correctly"""
        # we can get the form view
        get_response = self.client.get(
            reverse('auth_test_admin:improved_user_user_add'))
        self.assertEqual(get_response.status_code, 200)
        # we can create new users in the form view
        post_response = self.client.post(
            reverse('auth_test_admin:improved_user_user_add'),
            {
                'email': 'newuser@example.com',
                'password1': 'passw0rd1!',
                'password2': 'passw0rd1!',
            },
            follow=True,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(
            User.objects.filter(email='newuser@example.com').exists())
        new_user = User.objects.get(email='newuser@example.com')
        self.assertTrue(new_user.check_password('passw0rd1!'))

    def test_user_change_email(self):
        """Test that user can change email in Admin"""
        data = self.get_user_data(self.admin)
        data['email'] = 'new_' + data['email']
        response = self.client.post(
            reverse(
                'auth_test_admin:improved_user_user_change',
                args=(self.admin.pk,),
            ),
            data,
        )
        self.assertRedirects(
            response,
            reverse('auth_test_admin:improved_user_user_changelist'))
        row = LogEntry.objects.latest('id')
        if DjangoVersion >= (1, 9):
            self.assertEqual(row.get_change_message(), 'Changed email.')
        else:
            self.assertEqual(row.change_message, 'Changed email.')

    def test_user_not_change(self):
        """Test that message is raised when form submitted unchanged"""
        response = self.client.post(
            reverse(
                'auth_test_admin:improved_user_user_change',
                args=(self.admin.pk,),
            ),
            self.get_user_data(self.admin),
        )
        self.assertRedirects(
            response,
            reverse('auth_test_admin:improved_user_user_changelist'))
        row = LogEntry.objects.latest('id')
        if DjangoVersion >= (1, 9):
            self.assertEqual(row.get_change_message(), 'No fields changed.')
        else:
            self.assertEqual(row.change_message, 'No fields changed.')

    def test_user_change_password(self):
        """Test that URL to change password form is correct"""
        user_change_url = reverse(
            'auth_test_admin:improved_user_user_change', args=(self.admin.pk,))
        password_change_url = reverse(
            'auth_test_admin:auth_user_password_change',
            args=(self.admin.pk,))

        response = self.client.get(user_change_url)
        # Test the link inside password field help_text.
        rel_link = re.search(
            r'you can change the password using '
            r'<a href="([^"]*)">this form</a>',
            force_text(response.content),
        ).groups()[0]
        self.assertEqual(
            os.path.normpath(user_change_url + rel_link),
            os.path.normpath(password_change_url),
        )

        response = self.client.post(
            password_change_url,
            {
                'password1': 'password1',
                'password2': 'password1',
            },
        )
        self.assertRedirects(response, user_change_url)
        row = LogEntry.objects.latest('id')
        if DjangoVersion >= (1, 9):
            self.assertEqual(row.get_change_message(), 'Changed password.')
        else:
            self.assertEqual(row.change_message, 'Changed password.')
        self.logout()
        self.login(password='password1')

    def test_user_change_password_subclass_path(self):
        """Test subclasses can override password URL"""
        class CustomChangeForm(UserChangeForm):
            """Subclass of UserChangeForm; uses rel_password_url"""
            rel_password_url = 'moOps'

        form = CustomChangeForm()
        self.assertEqual(form.rel_password_url, 'moOps')
        rel_link = re.search(
            r'you can change the password using '
            r'<a href="([^"]*)">this form</a>',
            form.fields['password'].help_text,
        ).groups()[0]
        self.assertEqual(rel_link, 'moOps')

    def test_user_change_different_user_password(self):
        """Test that administrator can update other Users' passwords"""
        user = User.objects.get(email='staffmember@example.com')
        response = self.client.post(
            reverse(
                'auth_test_admin:auth_user_password_change',
                args=(user.pk,),
            ),
            {
                'password1': 'password1',
                'password2': 'password1',
            },
        )
        self.assertRedirects(
            response,
            reverse(
                'auth_test_admin:improved_user_user_change',
                args=(user.pk,)))
        row = LogEntry.objects.latest('id')
        self.assertEqual(row.user_id, self.admin.pk)
        self.assertEqual(row.object_id, str(user.pk))
        if DjangoVersion >= (1, 9):
            self.assertEqual(row.get_change_message(), 'Changed password.')
        else:
            self.assertEqual(row.change_message, 'Changed password.')

    def test_changelist_disallows_password_lookups(self):
        """Users shouldn't be allowed to guess password

        Checks against repeated password__startswith queries
        https://code.djangoproject.com/ticket/20078

        """
        # A lookup that tries to filter on password isn't OK
        with patch_logger(
            'django.security.DisallowedModelAdminLookup', 'error',
        ) as logger_calls:
            response = self.client.get(
                reverse('auth_test_admin:improved_user_user_changelist')
                + '?password__startswith=sha1$')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(logger_calls), 1)
