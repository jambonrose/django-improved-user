"""Integration project URL Configuration"""

from django.contrib import admin
from django.urls import re_path
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^$", TemplateView.as_view(template_name="home.html"), name="home"
    ),
]
