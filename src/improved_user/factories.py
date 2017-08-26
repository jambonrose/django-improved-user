"""Factories to make testing with Improved User easier"""
from .models import User

try:
    from factory import Faker, PostGenerationMethodCall
    from factory.django import DjangoModelFactory
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    raise Exception(
        "Please install factory_boy to use Improved User's UserFactory.\n"
        'pip install factory_boy==2.9.2')


# pylint: disable=too-few-public-methods
class UserFactory(DjangoModelFactory):
    """Factory Boy factory for Improved User

    Generates a user with a default password of ``password!``.
    The user is active, but is not staff or a superuser.
    Any value can be overridden by passing in a value, as shown below.

    .. code:: python

        UserFactory(
            password='mys3cr3tp4ssw0rd!',
            is_superuser=True,
        )
    """
    class Meta:
        """Configuration Options"""
        model = User

    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password!')
    full_name = Faker('name')
    short_name = Faker('first_name')
    is_active = True
    is_staff = False
    is_superuser = False
# pylint: enable=too-few-public-methods
