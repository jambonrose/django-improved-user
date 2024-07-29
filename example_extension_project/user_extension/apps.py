"""Application Definition File"""

from django.apps import AppConfig


class UserExtensionConfig(AppConfig):
    """AppConfig definition for user extension code"""

    name = "user_extension"
    default_auto_field = "django.db.models.AutoField"
