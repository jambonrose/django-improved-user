"""Replacement project URL Configuration"""

from django.contrib import admin

try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
]
