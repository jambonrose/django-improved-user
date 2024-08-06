"""Tests to ensure proper subclassing of models, forms, and factories"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from improved_user.forms import UserChangeForm, UserCreationForm

from .factories import UserFactory

User = get_user_model()  # pylint: disable=invalid-name


class ExtensionTestCase(TestCase):
    """Test Custom Extended User"""

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

        # can add short and full name
        user.full_name = "John Smith"
        user.short_name = "John"
        user.save()
        self.assertEqual(user.get_full_name(), "John Smith")
        self.assertEqual(user.get_short_name(), "John")

    def test_extra_boolean_field(self):
        """Verify that the current User has an extra boolean field"""
        email_lowercase = "test@example.com"
        password = "password1!"
        user = User.objects.create_user(email_lowercase, password)
        self.assertFalse(user.verified)
        self.assertFalse(user.is_verified())
        user.verified = True
        user.save()
        user = User.objects.get(email=email_lowercase)
        self.assertTrue(user.verified)
        self.assertTrue(user.is_verified())

    def test_basic_factory_build(self):
        """Test creation of User via factory"""
        user = UserFactory.build()
        self.assertIsInstance(user.verified, bool)
        self.assertEqual(User.objects.all().count(), 0)
        user.save()
        self.assertEqual(User.objects.all().count(), 1)

    def test_basic_factory_create(self):
        """Test creation of User via factory saves to DB"""
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertEqual(User.objects.all().count(), 1)

    def test_verified_attribute(self):
        """Ensure that verified attribute may be overridden"""
        user = UserFactory(verified=True)
        self.assertTrue(user.verified)
        user = UserFactory(verified=False)
        self.assertFalse(user.verified)

    @patch("django.contrib.auth.password_validation.password_changed")
    def test_create_form_success(self, password_changed):
        """Successful submission of form data"""
        data = {
            "email": "jsmith@example.com",
            "full_name": "John Smith",  # optional field
            "short_name": "John",  # optional field
            "password1": "k4b3c14gl9077954",
            "password2": "k4b3c14gl9077954",
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(password_changed.call_count, 0)
        user = form.save()
        self.assertEqual(password_changed.call_count, 1)
        self.assertEqual(repr(user), "<User: jsmith@example.com>")
        self.assertEqual(user.get_short_name(), "John")
        self.assertEqual(user.get_full_name(), "John Smith")
        self.assertTrue(user.check_password("k4b3c14gl9077954"))
        self.assertFalse(user.verified)

    def test_update_form_success(self):
        """Test successful submission of update form"""
        user = UserFactory()
        data = {
            "email": user.email,
            "date_joined": user.date_joined,
        }
        form = UserChangeForm(data, instance=user)
        self.assertTrue(form.is_valid())
