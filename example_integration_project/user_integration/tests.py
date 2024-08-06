"""Test integration of Improved User with Django

This test suite is legacy, and will be replaced in the near future.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestDataMigration(TestCase):
    """Test that the Improved User may be used in data migrations"""

    def test_user_exists(self):
        """Check UserManager properly created user"""
        User = get_user_model()  # pylint: disable=invalid-name
        self.assertTrue(
            User.objects.filter(email="migrated@jambonsw.com").exists()
        )


class TestViews(TestCase):
    """Test views to ensure User integration"""

    def test_home(self):
        """Test that homeview returns basic template"""
        get_response = self.client.get(reverse("home"))
        self.assertEqual(200, get_response.status_code)
        self.assertTemplateUsed(get_response, "home.html")
        self.assertTemplateUsed(get_response, "base.html")

    def test_tester(self):
        """Ensure that tests behave as expected"""
        email = "hello@jambonsw.com"
        password = "s4f3passw0rd!"
        User = get_user_model()  # pylint: disable=invalid-name
        User.objects.create_user(email, password)
        self.assertTrue(self.client.login(username=email, password=password))
