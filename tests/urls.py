"""Test URLs for auth admins"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.urls import urlpatterns

from improved_user.admin import UserAdmin
from improved_user.models import User

# Create a silo'd admin site for just the user/group admins.
SITE = admin.AdminSite(name='auth_test_admin')
SITE.register(User, UserAdmin)
SITE.register(Group, GroupAdmin)

urlpatterns += [
    url(r'^admin/', SITE.urls),
]
