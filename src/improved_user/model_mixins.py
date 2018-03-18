"""Mix-in Classes intended for use with Django Models"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class DjangoIntegrationMixin(models.Model):
    """Mixin provides fields for Django integration to work correctly

    Provides permissions for Django Admin integration, as well as date
    field used by authentication code.
    """
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into the admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        abstract = True


class FullNameMixin(models.Model):
    """A mixin to provide an optional full name field"""
    full_name = models.CharField(_('full name'), max_length=200, blank=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        """Returns the full name of the user."""
        return self.full_name


class ShortNameMixin(models.Model):
    """A mixin to provide an optional short name field"""
    short_name = models.CharField(_('short name'), max_length=50, blank=True)

    class Meta:
        abstract = True

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.short_name


class EmailAuthMixin(models.Model):
    """A mixin to use email as the username"""

    email = models.EmailField(_('email address'), max_length=254, unique=True)

    class Meta:
        abstract = True

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def clean(self):
        """Override default clean method to normalize email.

        Call :code:`super().clean()` if overriding.

        """
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


# pylint: disable=too-many-ancestors
class AbstractUser(
        DjangoIntegrationMixin, FullNameMixin, ShortNameMixin, EmailAuthMixin,
        PermissionsMixin, AbstractBaseUser):
    """
    An abstract base class meant to be inherited (do not instantiate
    this). The class provides a fully featured User model with
    admin-compliant permissions. Differs from Django's
    :class:`~django.contrib.auth.models.AbstractUser`:

    1. Login occurs with an email and password instead of username.
    2. Provides short_name and full_name instead of first_name and
       last_name.

    All fields other than email and password are optional.

    Sets :attr:`~django.db.models.Model.objects` to
    :class:`~improved_user.models.UserManager`.

    Documentation about Django's
    :class:`~django.contrib.auth.models.AbstractBaseUser` may be helpful
    in understanding this class.
    """
    objects = UserManager()

    # misnomer; fields Dj prompts for when user calls createsuperuser
    # https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ['full_name', 'short_name']

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')
