"""A User model created by django-improved-user mixins"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from improved_user.managers import UserManager
from improved_user.model_mixins import DjangoIntegrationMixin, EmailAuthMixin


class User(
    DjangoIntegrationMixin, EmailAuthMixin, PermissionsMixin, AbstractBaseUser
):
    """A user created using mix-ins from Django and improved-user

    Note that the lack of name methods will cause errors in the Admin
    """

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
