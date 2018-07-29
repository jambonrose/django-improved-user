#################
Package Reference
#################

.. contents:: In this Document
   :local:

.. py:module:: improved_user.apps

********
Overview
********

Django Improved User is organized like a regular Django app.

.. py:class:: improved_user.apps.ImprovedUserConfig

    Reference this class in ``INSTALLED_APPS`` to use the package.

The package provides both a concerete
:class:`~improved_user.models.User` model, as well as mix-in and
abstract model classes to be used to extend the model or replace it
entirely. Please refer to :doc:`../select_configuration_method` for more
information about how to configure these models to best suit your
purposes.

The package also provides forms, test factories, and an admin panel. Please
see the reference documentation for these items below.

Finally, the actual code on `Github`_ has three example projects that may
be helpful if this documentation was not.

.. _Github: https://github.com/jambonsw/django-improved-user

*******************
Reference Documents
*******************

.. toctree::
   :glob:
   :maxdepth: 2

   models
   managers
   model_mixins
   forms
   factories
   admin
