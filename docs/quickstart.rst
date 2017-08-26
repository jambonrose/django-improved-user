###############################
Quickstart: Using Improved User
###############################

This document provides the least amount of info to get started with the
package.

.. contents::
   :local:

************
Installation
************

In a Terminal, use :code:`pip` to install the package from `PyPI`_.

.. code:: console

    pip install django-improved-user

If you intend to use the :class:`~improved_user.factories.UserFactory` provided by the package to
allow for testing with |factory_boy|_, you can specify so during
install.

.. code:: console

    pip install django-improved-user[factory]

If you do not but wish to use the :code:`UserFactory`, you will need to
install |factory_boy|_ yourself.

.. _PyPI: https://pypi.org/project/django-improved-user/
.. _factory_boy: https://github.com/FactoryBoy/factory_boy
.. |factory_boy| replace:: :code:`factory_boy`

*********************
Integration and Usage
*********************

In a new Django project, perform the following steps in the ``settings.py`` file or base settings file.

1. Add :code:`improved_user.apps.ImprovedUserConfig`
   to :code:`INSTALLED_APPS`
2. Define or replace :code:`AUTH_USER_MODEL` with the new model, as
   below.

    .. code:: python

        AUTH_USER_MODEL='improved_user.User'

3. In Django > 1.9, change :code:`UserAttributeSimilarityValidator` to
   match correct :code:`User` fields, as shown below.

    .. code:: python

        AUTH_PREFIX = 'django.contrib.auth.password_validation.'
        AUTH_PASSWORD_VALIDATORS = [
            {
                'NAME': AUTH_PREFIX + 'UserAttributeSimilarityValidator',
                'OPTIONS': {
                    'user_attributes': ('email', 'full_name', 'short_name')
                },
            },
            # include other password validators here
        ]
