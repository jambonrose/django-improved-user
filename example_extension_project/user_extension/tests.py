"""Tests to ensure proper subclassing of models, forms, and factories"""
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()  # pylint: disable=invalid-name


class ExtensionTestCase(TestCase):
    """Test Custom Extended User"""

    def test_user_creation(self):
        """Users can be created and can set/modify their password"""
        email_lowercase = 'test@example.com'
        password = 'password1!'
        user = User.objects.create_user(email_lowercase, password)
        self.assertEqual(user.email, email_lowercase)
        self.assertTrue(user.has_usable_password())
        self.assertFalse(user.check_password('wrong'))
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

        # can add short and full name
        user.full_name = 'John Smith'
        user.short_name = 'John'
        user.save()
        self.assertEqual(user.get_full_name(), 'John Smith')
        self.assertEqual(user.get_short_name(), 'John')

    def test_extra_boolean_field(self):
        """Verify that the current User has an extra boolean field"""
        email_lowercase = 'test@example.com'
        password = 'password1!'
        user = User.objects.create_user(email_lowercase, password)
        self.assertFalse(user.verified)
        self.assertFalse(user.is_verified())
        user.verified = True
        user.save()
        user = User.objects.get(email=email_lowercase)
        self.assertTrue(user.verified)
        self.assertTrue(user.is_verified())
