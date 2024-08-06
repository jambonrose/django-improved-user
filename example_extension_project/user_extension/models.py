"""Demonstration of how to extend the Improved User model"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from improved_user.model_mixins import AbstractUser


# pylint: disable=too-many-ancestors
class User(AbstractUser):
    """A User model that extends the Improved User"""

    verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_("Designates whether the user has verified their email."),
    )

    def is_verified(self):
        """Is the user properly verified?"""
        return self.is_active and self.verified
