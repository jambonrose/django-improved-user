"""App Configuration for Improved User"""

from django.apps import AppConfig
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class ImprovedUserConfig(AppConfig):
    """App Config for Improved User"""

    name = "improved_user"
    verbose_name = _("Improved User")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        """Register User model for Admin

        Ensure UserAdmin is only used when application is added to
        Installed Apps, and that UserAdmin can be imported if necessary
        (please note: not recommended. Please see the docs).

        https://django-improved-user.rtfd.io/en/latest/admin_usage.html
        """
        from .admin import UserAdmin

        User = get_user_model()  # pylint: disable=invalid-name
        admin.site.register(User, UserAdmin)
