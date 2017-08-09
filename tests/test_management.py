"""Test User model management commands"""
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from improved_user.models import User


class CreatesuperuserManagementCommandTestCase(TestCase):
    """Test createsuperuser management command"""

    def test_basic_usage(self):
        """Check the operation of the createsuperuser management command"""
        # We can use the management command to create a superuser
        new_io = StringIO()
        call_command(
            'createsuperuser',
            interactive=False,
            email='joe@somewhere.org',
            short_name='Joe',
            full_name='Joe Smith',
            stdout=new_io,
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, 'Superuser created successfully.')
        user = User.objects.get(email='joe@somewhere.org')
        self.assertEqual(user.short_name, 'Joe')

        # created password should be unusable
        self.assertFalse(user.has_usable_password())

    def test_no_email_argument(self):
        """Ensure that email is required"""
        new_io = StringIO()
        with self.assertRaisesMessage(CommandError,
                                      'You must use --email with --noinput.'):
            call_command(
                'createsuperuser',
                interactive=False,
                short_name='Joe',
                full_name='Joe Smith',
                stdout=new_io)

    def test_invalid_username(self):
        """Creation fails if the username fails validation."""
        email_field = User._meta.get_field('email')
        new_io = StringIO()
        invalid_username = ('x' * email_field.max_length) + 'y'

        expected_error = (
            'Enter a valid email address.; '
            'Ensure this value has at most %d characters (it has %d).'
            % (email_field.max_length, len(invalid_username))
        )

        with self.assertRaisesMessage(CommandError, expected_error):
            call_command(
                'createsuperuser',
                interactive=False,
                email=invalid_username,
                short_name='Joe',
                full_name='Joe Smith',
                password='password1!',
                stdout=new_io)
