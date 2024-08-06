"""Tests for the extended User model"""

from types import MethodType

from django.test import TestCase

from .models import User


class ExtendedUserModelTests(TestCase):
    """Tests for the extended User model"""

    def test_user_creation(self):
        """Users can be created and can set/modify their password"""
        email_lowercase = "test@example.com"
        password = "password1!"
        user = User.objects.create_user(email_lowercase, password)
        self.assertEqual(user.email, email_lowercase)
        self.assertTrue(user.has_usable_password())
        self.assertFalse(user.check_password("wrong"))
        self.assertTrue(user.check_password(password))

        # Check we can manually set an unusable password
        user.set_unusable_password()
        user.save()
        self.assertFalse(user.check_password(password))
        self.assertFalse(user.has_usable_password())
        user.set_password(password)
        self.assertTrue(user.check_password(password))
        user.set_password(None)
        self.assertFalse(user.has_usable_password())

        self.assertFalse(hasattr(user, "get_full_name"))
        self.assertFalse(hasattr(user, "get_short_name"))

    def test_fields_and_attributes(self):
        """Ensure the model has the fields and attributes we expect"""
        expected_fields = (
            "id",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "groups",
            "user_permissions",
        )
        excluded_fields = (
            "full_name",
            "short_name",
        )
        user_fields = [field.name for field in User._meta.get_fields()]
        for expected_field in expected_fields:
            with self.subTest(expected_field=expected_field):
                self.assertIn(expected_field, user_fields)
        for excluded_field in excluded_fields:
            with self.subTest(excluded_field=excluded_field):
                self.assertNotIn(excluded_field, user_fields)
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
