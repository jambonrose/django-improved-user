"""Integration project URL Configuration"""
from django.contrib import admin
from django.views.generic import TemplateView
from user_integration import urls as account_urls

# pylint: disable=ungrouped-imports
try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include, url as re_path
# pylint: enable=ungrouped-imports


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^accounts/", include(account_urls)),
    re_path(
        r"^$", TemplateView.as_view(template_name="home.html"), name="home"
    ),
]
