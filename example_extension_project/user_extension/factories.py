"""Factories to make testing with Extended User easier

Demonstrated here to ensure that Improved User Factory can be subclassed.

"""

from factory import Faker

from improved_user.factories import UserFactory as BaseUserFactory


# pylint: disable=too-few-public-methods
class UserFactory(BaseUserFactory):
    """A subclass of Improved Users' UserFactory"""

    verified = Faker("pybool")  # not strictly necessary due to False default
