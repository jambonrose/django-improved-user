"""Compose new Django User models that follow best-practices for international names and authenticate via email instead of username."""

# This file:
#     1. define directory as module
#     2. set default app config

# pylint: disable=invalid-name
__version__ = "2.0a2"
# https://docs.djangoproject.com/en/stable/ref/applications/#configuring-applications
default_app_config = "improved_user.apps.ImprovedUserConfig"
# pylint: enable=invalid-name
