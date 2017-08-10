"""Test model factories provided by Improved User"""
from django.test import TestCase

from improved_user.factories import UserFactory
from improved_user.models import User


class UserFactoryTests(TestCase):
    """Test for UserFactory used with Factory Boy"""

    def test_basic_build(self):
        """Test creation of User via factory"""
        user = UserFactory.build()
        self.assertIsInstance(user, User)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.short_name, str)
        self.assertIsInstance(user.full_name, str)
        self.assertGreater(len(user.email), 1)
        self.assertGreater(len(user.short_name), 1)
        self.assertGreater(len(user.full_name), 1)
        self.assertTrue(user.check_password('password!'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(User.objects.all().count(), 0)
        user.save()
        self.assertEqual(User.objects.all().count(), 1)

    def test_basic_create(self):
        """Test creation of User via factory saves to DB"""
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertEqual(User.objects.all().count(), 1)

    def test_attributes_override_build(self):
        """Test that all model fields can be modified"""
        user = UserFactory.build(
            email='hello@jambonsw.com',
            password='my_secret_password87',
            short_name='René',
            full_name='René Magritte',
            is_active=False,
            is_staff=True,
            is_superuser=True,
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'hello@jambonsw.com')
        self.assertEqual(user.short_name, 'René')
        self.assertEqual(user.full_name, 'René Magritte')
        self.assertTrue(user.check_password('my_secret_password87'))
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(User.objects.all().count(), 0)
        user.save()
        self.assertEqual(User.objects.all().count(), 1)

    def test_attributes_override_create(self):
        """Test that all model fields can be modified during creation"""
        user = UserFactory(
            email='hello@jambonsw.com',
            password='my_secret_password87',
            short_name='René',
            full_name='René Magritte',
            is_active=False,
            is_staff=True,
            is_superuser=True,
        )
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password('my_secret_password87'))
        self.assertEqual(User.objects.all().count(), 1)
