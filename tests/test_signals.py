"""Test Signal Handling"""
from django.db.models.signals import post_save
from django.test import TestCase

from improved_user.models import User


class TestCreateSuperUserSignals(TestCase):
    """Simple test case for ticket #20541"""

    # pylint: disable=unused-argument
    def post_save_listener(self, *args, **kwargs):
        """Utility function to note when signal sent"""
        self.signals_count += 1
    # pylint: enable=unused-argument

    def setUp(self):
        """Connect function above to postsave User model signal"""
        self.signals_count = 0
        post_save.connect(self.post_save_listener, sender=User)

    def tearDown(self):
        """Connect utility function from postsave"""
        post_save.disconnect(self.post_save_listener, sender=User)

    def test_create_user(self):
        """Test User Creation"""
        User.objects.create_user('mail@example.com')
        self.assertEqual(self.signals_count, 1)

    def test_create_superuser(self):
        """Test Super User Creation"""
        User.objects.create_superuser('mail@example.com', 'password')
        self.assertEqual(self.signals_count, 1)
