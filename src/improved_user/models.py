"""The Improved User Model

Mixin classes used to create this class may be found in mixins.py

The UserManager is found in managers.py

"""
from .model_mixins import AbstractUser


# pylint: disable=too-many-ancestors
class User(AbstractUser):
    """The Improved User Model is intended to be used out-of-the-box.

    Do **not** import this model directly: use
    :py:func:`~django.contrib.auth.get_user_model`.
    """
