"""Test Improved User Model"""
from datetime import datetime
from types import MethodType
from unittest import skipUnless
from unittest.mock import patch

from django import VERSION as DjangoVersion
from django.contrib.auth.hashers import get_hasher
from django.core import mail
from django.test import TestCase

from improved_user.models import User


class UserModelTestCase(TestCase):
    """Improve User Model Test Suite"""

    def test_fields_and_attributes(self):
        """Ensure the model has the fields and attributes we expect"""
        expected_fields = (
            'id',
            'password',
            'last_login',
            'is_superuser',
            'full_name',
            'short_name',
            'is_staff',
            'is_active',
            'date_joined',
            'email',
            'groups',
            'user_permissions',
        )
        user_fields = [field.name for field in User._meta.get_fields()]
        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, user_fields)
        # Pre-empt Django check auth.E001
        self.assertTrue(isinstance(User.REQUIRED_FIELDS, (list, tuple)))
        # Pre-empt Django check auth.E002
        self.assertNotIn(User.USERNAME_FIELD, User.REQUIRED_FIELDS)
        # Pre-empt Django check auth.E003
        self.assertIs(User._meta.get_field(User.USERNAME_FIELD).unique, True)
        # Pre-empt Django check auth.C009
        self.assertFalse(isinstance(User.is_anonymous, MethodType))
        # Pre-empt Django check auth.C010
        self.assertFalse(isinstance(User.is_authenticated, MethodType))

    def test_email_user(self):
        """Send Email to User via method"""
        # valid send_mail parameters
        kwargs = {
            'fail_silently': False,
            'auth_user': None,
            'auth_password': None,
            'connection': None,
            'html_message': None,
        }
        user = User(email='foo@bar.com')
        user.email_user(
            subject='Subject here',
            message='This is a message',
            from_email='from@domain.com',
            # TODO: when Py3.4 removed, add comma, remove C815 exception
            **kwargs  # noqa: C815
        )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Subject here')
        self.assertEqual(message.body, 'This is a message')
        self.assertEqual(message.from_email, 'from@domain.com')
        self.assertEqual(message.to, [user.email])

    def test_last_login_default(self):
        """Check last login not set upon creation"""
        user1 = User.objects.create(email='test1@example.com')
        self.assertIsNone(user1.last_login)

        user2 = User.objects.create(email='test2@example.com')
        self.assertIsNone(user2.last_login)

    def test_date_joined_default(self):
        """Check date joined set upon creation"""
        user1 = User.objects.create(email='test1@example.com')
        self.assertIsNotNone(user1.date_joined)
        self.assertIsInstance(user1.date_joined, datetime)

        user2 = User.objects.create(email='test2@example.com')
        self.assertIsNotNone(user2.date_joined)
        self.assertIsInstance(user2.date_joined, datetime)

    def test_user_clean_normalize_email(self):
        """User email/username is normalized upon creation"""
        user = User(email='foo@BAR.com', password='foo')
        user.clean()
        self.assertEqual(user.email, 'foo@bar.com')

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    def test_user_double_save(self):
        """
        Calling user.save() twice should trigger password_changed() once.
        """
        user = User.objects.create_user(
            email='test@example.com', password='foo')
        user.set_password('bar')
        with patch(
            'django.contrib.auth.password_validation.password_changed',
        ) as pw_changed:
            user.save()
            self.assertEqual(pw_changed.call_count, 1)
            user.save()
            self.assertEqual(pw_changed.call_count, 1)

    @skipUnless(
        DjangoVersion >= (1, 9),
        'Password strength checks not available on Django 1.8')
    def test_check_password_upgrade(self):
        """
        password_changed() shouldn't be called if User.check_password()
        triggers a hash iteration upgrade.
        """
        user = User.objects.create_user(
            email='test@example.com', password='foo')
        initial_password = user.password
        self.assertTrue(user.check_password('foo'))
        hasher = get_hasher('default')
        self.assertEqual('pbkdf2_sha256', hasher.algorithm)

        old_iterations = hasher.iterations
        try:
            # Upgrade the password iterations
            hasher.iterations = old_iterations + 1
            with patch(
                'django.contrib.auth.password_validation.password_changed',
            ) as pw_changed:
                user.check_password('foo')
                self.assertEqual(pw_changed.call_count, 0)
            self.assertNotEqual(initial_password, user.password)
        finally:
            hasher.iterations = old_iterations
