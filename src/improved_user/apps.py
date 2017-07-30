"""App Configuration for Improved User"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ImprovedUserConfig(AppConfig):
    """App Config for Improved User"""
    name = 'improved_user'
    verbose_name = _('Improved User')
