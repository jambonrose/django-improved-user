"""Demonstrate use of UserAdmin on extended User model"""

from django.contrib import admin
from django.contrib.auth import get_user_model

from improved_user.admin import UserAdmin

User = get_user_model()  # pylint: disable=invalid-name
# WARNING
# This works, but note that any additional fields do not appear in the
# Admin.  For instance, the User model in this example has a verified
# boolean field added to it, but this field will not appear in the
# admin.  Additionally, if the verified field did not have a default,
# creating the User model via the admin panel would be impossible. As
# such, do not use this method in production applications, and instead
# define your own UserAdmin class.
admin.site.register(User, UserAdmin)
