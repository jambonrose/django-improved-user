"""Test User model manager"""
from datetime import datetime

from django.test import TestCase

from improved_user.managers import UserManager
from improved_user.models import User


class UserManagerTestCase(TestCase):
    """Test User model manager"""

    def test_create_user_email_domain_normalize_rfc3696(self):
        """Normalize email allows @ in email local section"""
        # According to  http://tools.ietf.org/html/rfc3696#section-3
        # the "@" symbol can be part of the local part of an email address
        returned = UserManager.normalize_email(r'Abc\@DEF@EXAMPLE.com')
        self.assertEqual(returned, r'Abc\@DEF@example.com')

    def test_create_user_email_domain_normalize(self):
        """Normalize email lowercases domain"""
        returned = UserManager.normalize_email('normal@DOMAIN.COM')
        self.assertEqual(returned, 'normal@domain.com')

    def test_create_user_email_domain_normalize_with_whitespace(self):
        """Normalize email allows whitespace in email local section"""
        # pylint: disable=anomalous-backslash-in-string
        returned = UserManager.normalize_email('email\ with_whitespace@D.COM')
        self.assertEqual(returned, 'email\ with_whitespace@d.com')
        # pylint: enable=anomalous-backslash-in-string

    def test_empty_username(self):
        """Manager raises error if email is missing"""
        self.assertRaisesMessage(
            ValueError,
            'An email address must be provided.',
            User.objects.create_user,
            email='',
        )

    def test_create_user_is_staff(self):
        """Check is_staff attribute is respected"""
        email = 'normal@normal.com'
        user = User.objects.create_user(email, is_staff=True)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)

    def test_create_user_is_active(self):
        """Check is_active attribute is respected"""
        email = 'normal@normal.com'
        user = User.objects.create_user(email, is_active=False)
        self.assertEqual(user.email, email)
        self.assertFalse(user.is_active)

    def test_username_keyword_raises_warning(self):
        """Remind dev that username doesn't exist on model"""
        error = ('The Improved User model does not have a username; '
                 'it uses only email')
        with self.assertRaisesMessage(ValueError, error):
            User.objects.create_user(
                username='whoops',
                email='test@test.com',
                password='test',
            )
        with self.assertRaisesMessage(ValueError, error):
            User.objects.create_superuser(
                username='whoops',
                email='test@test.com',
                password='test',
            )

    def test_create_super_user_raises_error_on_false_is_superuser(self):
        """Warn developer when creating superuse without is_superuser"""
        error = 'Superuser must have is_superuser=True.'
        with self.assertRaisesMessage(ValueError, error):
            User.objects.create_superuser(
                email='test@test.com',
                password='test',
                is_superuser=False,
            )

    def test_create_superuser_raises_error_on_false_is_staff(self):
        """Warn developer when creating superuse without is_staff"""
        error = 'Superuser must have is_staff=True.'
        with self.assertRaisesMessage(ValueError, error):
            User.objects.create_superuser(
                email='test@test.com',
                password='test',
                is_staff=False,
            )

    def test_make_random_password(self):
        """Test manager make_random_password method"""
        allowed_chars = 'abcdefg'
        password = UserManager().make_random_password(5, allowed_chars)
        self.assertEqual(len(password), 5)
        for char in password:
            self.assertIn(char, allowed_chars)

    def test_last_login_is_none(self):
        """Check that last login is unset when created

        https://github.com/jambonsw/django-improved-user/issues/25
        """
        user1 = User.objects.create_user('hello@jambonsw.com', 'password1')
        self.assertIsNone(user1.last_login)

        user2 = User.objects.create_superuser('clark@kent.com', 'password1')
        self.assertIsNone(user2.last_login)

    def test_date_joined_default(self):
        """Check date joined set upon creation"""
        user1 = User.objects.create_user('hello@jambonsw.com', 'password1')
        self.assertIsNotNone(user1.date_joined)
        self.assertIsInstance(user1.date_joined, datetime)

        user2 = User.objects.create_superuser('clark@kent.com', 'password1')
        self.assertIsNotNone(user2.date_joined)
        self.assertIsInstance(user2.date_joined, datetime)
