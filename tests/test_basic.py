"""Test basic functionality; test API used by a Django project developer"""
from unittest import skipUnless

from django import VERSION as DjangoVersion
from django.contrib.auth import get_user, get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.utils import translation

from improved_user.models import User


class BasicTestCase(TestCase):
    """Test Improved User to mimic Django Auth User

    The goal is to provide a User model that can be used as a drop-in
    replacement for Django Auth User, all while providing mixin classes
    to allow developers to easily extend their own class. These tests
    focus on the first part.
    """

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

    def test_user_creation_without_password(self):
        """Users can be created without password"""
        user = User.objects.create_user('test@example.com')
        self.assertFalse(user.has_usable_password())

    def test_unicode_email(self):  # pylint: disable=no-self-use
        """Unicode emails are allowed in Model

        Note that Django's Email field validator will error on
        the following, meaning that while the model accepts
        these values, the forms will not. Some work required.

        """
        User.objects.create_user('Pelé@example.com')
        User.objects.create_user('δοκιμή@παράδειγμα.δοκιμή')
        User.objects.create_user('我買@屋企.香港')
        User.objects.create_user('甲斐@黒川.日本')
        User.objects.create_user('чебурашка@ящик-с-апельсинами.рф')
        User.objects.create_user('संपर्क@डाटामेल.भारत')
        # Unlike usernames, emails are not normalized,
        # identical glyphs with different codepoints are allowed
        omega_emails = 'iamtheΩ@email.com'  # U+03A9 GREEK CAPITAL LETTER OMEGA
        ohm_username = 'iamtheΩ@email.com'  # U+2126 OHM SIGN
        User.objects.create_user(omega_emails)
        User.objects.create_user(ohm_username)

    def test_user_permissions(self):
        """Test normal user's authentication permissions"""
        user = User.objects.create_user('test@example.com')
        # Check authentication/permissions
        if DjangoVersion >= (1, 10):
            self.assertFalse(user.is_anonymous)
            self.assertTrue(user.is_authenticated)
        else:
            self.assertFalse(user.is_anonymous())
            self.assertTrue(user.is_authenticated())
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_superuser_permissions(self):
        """Test superuser's authentication permissions"""
        user = User.objects.create_superuser('test@example.com', 'password1!')
        if DjangoVersion >= (1, 10):
            self.assertFalse(user.is_anonymous)
            self.assertTrue(user.is_authenticated)
        else:
            self.assertFalse(user.is_anonymous())
            self.assertTrue(user.is_authenticated())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

    def test_username_getter(self):
        """Check username getter method"""
        user = User.objects.create_user('test@example.com')
        self.assertEqual(user.get_username(), 'test@example.com')

    @skipUnless(
        DjangoVersion >= (1, 11),
        'Method not implemented until Django 1.11')
    def test_default_email_method(self):
        """Test correct email field used in method"""
        user = User()
        self.assertEqual(user.get_email_field_name(), 'email')

    def test_default_email_field(self):
        """Test correct email field used"""
        self.assertEqual(User.EMAIL_FIELD, 'email')

    def test_is_active(self):
        """Test that is_active can be modified"""
        user = User.objects.create(email='foo@bar.com')
        # is_active is true by default
        self.assertIs(user.is_active, True)
        user.is_active = False
        user.save()
        user_fetched = User.objects.get(pk=user.pk)
        # the is_active flag is saved
        self.assertIs(user_fetched.is_active, False)

    def test_is_staff(self):
        """Test that is_staff can be modified"""
        user = User.objects.create(email='foo@bar.com')
        # is_active is true by default
        self.assertIs(user.is_staff, False)
        user.is_staff = True
        user.save()
        user_fetched = User.objects.get(pk=user.pk)
        # the is_active flag is saved
        self.assertIs(user_fetched.is_staff, True)

    def test_is_superuser(self):
        """Test that is_superuser can be modified"""
        user = User.objects.create(email='foo@bar.com')
        # is_active is true by default
        self.assertIs(user.is_superuser, False)
        user.is_superuser = True
        user.save()
        user_fetched = User.objects.get(pk=user.pk)
        # the is_active flag is saved
        self.assertIs(user_fetched.is_superuser, True)

    def test_get_user_model(self):
        """The improved user model can be retrieved"""
        self.assertEqual(get_user_model(), User)
        with self.assertRaises(AttributeError):
            from django.contrib.auth.models import User as DjangoUser
            DjangoUser.objects.all()

    def test_user_verbose_names_translatable(self):
        """User model verbose names are translatable (#19945)"""
        with translation.override('en'):
            self.assertEqual(User._meta.verbose_name, 'user')
            self.assertEqual(User._meta.verbose_name_plural, 'users')
        with translation.override('es'):
            self.assertEqual(User._meta.verbose_name, 'usuario')
            self.assertEqual(User._meta.verbose_name_plural, 'usuarios')

    def test_get_user(self):
        """Improved User can be extracted from request"""
        created_user = User.objects.create_user('test@example.com', 'testpw')
        self.client.login(username='test@example.com', password='testpw')
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, created_user.email)
