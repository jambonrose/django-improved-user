Django SimpleUser
=================

A custom Django user model that encompasses best practices:

* email-based login

* "Full name/short name", rather than the "First name"/"Last name"
   antipattern

Usage:
------

* Add `simpleuser` to `INSTALLED_APPS`
* Add `AUTH_USER_MODEL='simpleuser.User'` to your `settings.py` file.
