#################
Package Reference
#################



.. contents:: In this Document
   :local:

.. py:module:: improved_user.apps
.. py:module:: improved_user.forms
.. py:module:: improved_user.models

********
Overview
********

Django Improved User is organized like a regular Django app.

.. py:class:: improved_user.apps.ImprovedUserConfig

    Reference this class in ``INSTALLED_APPS`` to use the package.

However, the package serves a dual purpose: providing a best-practice
user model as well as providing mix-in classes. The
:py:class:`~improved_user.models.User` model in
:py:mod:`improved_user.models` is built with modular classes found in
:py:mod:`improved_user.mixins`, which may be reused to build your own
custom User. The classes in :py:mod:`improved_user.forms` may be used to
either integrate or extend the improved ``User`` as well, and the
documentation is therefore split to reflect that differences as well.

*****************
Using the Package
*****************

If you seek to use the package directly, :py:mod:`~improved_user.models`
provides the :py:class:`~improved_user.models.User` (connected to the
:py:class:`~improved_user.models.UserManager`) and
:py:mod:`~improved_user.forms` provides
:py:class:`~improved_user.forms.UserCreationForm` and
:py:class:`~improved_user.forms.UserChangeForm`.

*********************
Extending the Package
*********************

You you wish to extend the code supplied by this package,
:doc:`mixin_models` documents classes in :py:mod:`improved_user.mixins`
to help build your own user.
:py:class:`~improved_user.mixins.AbstractUser` is notably meant to be
extended, while other classes such as
:py:class:`~improved_user.mixins.DjangoIntegrationMixin`,
:py:class:`~improved_user.mixins.EmailAuthMixin`
:py:class:`~improved_user.mixins.FullNameMixin`
:py:class:`~improved_user.mixins.ShortNameMixin` can be mixed and
matched as desired. Similarly, the :doc:`mixin_forms` details the
:py:class:`~improved_user.forms.AbstractUserCreationForm` and
:py:class:`~improved_user.forms.AbstractUserChangeForm` classes found in
:py:mod:`improved_user.forms`, which are meant to be inherited and
extended.

*******************
Reference Documents
*******************

.. toctree::
   :glob:
   :maxdepth: 2

   models
   managers
   forms
   factories
   admin
   mixin_models
   mixin_forms
