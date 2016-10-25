from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class SimpleUserConfig(AppConfig):
    name = 'simpleuser'
    verbose_name = _("best-practice email-based authentication and authorization")
