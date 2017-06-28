from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ImprovedUserConfig(AppConfig):
    name = 'improved_user'
    verbose_name = _("Improved User")
