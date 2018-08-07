###############################
Quickstart: Using Improved User
###############################

This document provides a quick tutorial for the recommended way to setup
Improved User.

See :doc:`select_configuration_method` for an overview of options and tradeoffs.

.. contents::
   :local:

************
Installation
************

In a Terminal, use :code:`pip` to install the package from `PyPI`_. 
To use the :class:`~improved_user.factories.UserFactory` provided 
by the package to allow for testing with |factory_boy|_, include it
in the installation.

.. code:: console

    $ pip install django-improved-user[factory]

If |factory_boy|_ is unnecessary, it can be omitted by installing normally.

.. code:: console

    $ pip install django-improved-user



.. _PyPI: https://pypi.org/project/django-improved-user/
.. _factory_boy: https://github.com/FactoryBoy/factory_boy
.. |factory_boy| replace:: :code:`factory_boy`

***********************
Configuration and Usage
***********************

1. In a Django project, create a new app. For the purposes of this
   documentation, we will assume the name of your new app is
   ``user_app``, but you could name it whatever you wish.

   .. code:: console

        $ python3 manage.py startapp user_app

2. In your project's settings, add :code:`user_app.apps.UserAppConfig` to
   :code:`INSTALLED_APPS` (replace ``user_app`` and ``UserAppConfig``
   as necessary).

3. In ``user_app/models.py``, import Improved User's
   :py:class:`~improved_user.model_mixins.AbstractUser`.

    .. literalinclude:: ../example_extension_project/user_extension/models.py
        :lines: 5

4. Create a new :code:`User` model. If you omit comments, you may need
   to add :code:`pass` to the line below the class.

    .. literalinclude:: ../example_extension_project/user_extension/models.py
        :lines: 9-10

.. ATTENTION::
    If you add your own fields to the model, you may wish to modify
    :attr:`~django.contrib.auth.models.CustomUser.REQUIRED_FIELDS`.

5. Define or replace :setting:`AUTH_USER_MODEL` in your project settings
   with the new model, as below (replace :code:`user_app` with the name
   of your own app).

    .. code:: python

        AUTH_USER_MODEL='user_app.User'

.. TIP::
    Remember to use :py:func:`~django.contrib.auth.get_user_model` to
    get your new model. Don't import it directly!

6. In Django > 1.9, while still in settings, change
   :class:`UserAttributeSimilarityValidator` to match correct
   :py:class:`~improved_user.model_mixins.AbstractUser` fields,
   as shown below.

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

7. You're done! 🎉 Run migrations or go back to programming the rest
   of your project.

.. NOTE::
    Improved user also comes with forms, test factories, and an admin panel.
    Take a look at the :doc:`source/modules` for more information.
