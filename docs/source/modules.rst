#########
Reference
#########

.. py:module:: improved_user.apps
.. py:module:: improved_user.forms
.. py:module:: improved_user.models

Django Improved User is organized like a regular Django app. However,
the package serves a dual purpose: providing a best-practice user model
as well as providing mix-in classes. The reference documentation for
:py:mod:`improved_user.models` and :py:mod:`improved_user.forms`
are split into two to best reflect those differences.

.. py:class:: improved_user.apps.ImprovedUserConfig

    Reference this class in ``INSTALLED_APPS`` to use the package.

.. toctree::
   :caption: Package Reference Contents:
   :glob:
   :maxdepth: 2

   models
   managers
   forms
   factories
   admin
   mixin_models
   mixin_forms
