"""Test User model management commands"""
import builtins
from io import StringIO

from django import VERSION as DjangoVersion
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from improved_user.models import User


# pylint: disable=missing-docstring,too-few-public-methods
def mock_inputs(inputs):
    """
    Decorator to temporarily replace input/getpass to allow interactive
    createsuperuser.
    """
    def inner(test_func):
        def wrapped(*args):
            class MockGetPass:
                # pylint: disable=unused-argument
                @staticmethod
                def getpass(prompt=b'Password: ', stream=None):
                    if callable(inputs['password']):
                        return inputs['password']()
                    return inputs['password']
                # pylint: enable=unused-argument

            def mock_input(prompt):
                assert '__proxy__' not in prompt
                response = ''
                for key, val in inputs.items():
                    if key in prompt.lower():
                        if callable(val):
                            response = val()
                        else:
                            response = val
                        break
                return response

            old_getpass = createsuperuser.getpass
            old_input = builtins.input
            createsuperuser.getpass = MockGetPass
            builtins.input = mock_input
            try:
                test_func(*args)
            finally:
                createsuperuser.getpass = old_getpass
                builtins.input = old_input
        return wrapped
    return inner


class MockTTY:
    """
    A fake stdin object that pretends to be a TTY to be used in conjunction
    with mock_inputs.
    """
    def isatty(self):  # pylint: disable=no-self-use
        return True
# pylint: enable=missing-docstring,too-few-public-methods


@override_settings(
    AUTH_PASSWORD_VALIDATORS=[{
        'NAME':
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'}])
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
                stdout=new_io)

    def test_password_validation(self):
        """Creation should fail if the password fails validation."""
        new_io = StringIO()

        index = [0]

        # Returns '1234567890' the first two times it is called, then
        # 'password' subsequently.
        def bad_then_good_password():
            """Simulate user input on terminal"""
            index[0] += 1
            if index[0] <= 2:
                return '1234567890'
            return 'password'

        @mock_inputs({
            'password': bad_then_good_password,
        })
        def test(self):
            """The actual test function; run with multiple inputs"""
            call_command(
                'createsuperuser',
                email='hello@jambonsw.com',
                full_name='Joe Smith',
                interactive=True,
                short_name='Joe',
                stderr=new_io,
                stdin=MockTTY(),
                stdout=new_io,
            )
            if DjangoVersion >= (1, 9):
                expected_out = ('This password is entirely numeric.\n'
                                'Superuser created successfully.')
            else:
                expected_out = 'Superuser created successfully.'
            self.assertEqual(new_io.getvalue().strip(), expected_out)

        test(self)
