Read Me
=======

This project provides a custom user model that improves on Django's
default by making a few modern and international changes.

* Uses email as the username to simplify login for users
* Replace ``first_name`` and ``last_name`` with international friendly
  ``short_name`` ``full name`` fields

Usage
-----

Perform the following steps in your ``settings.py`` file.

1. Add ``improved_user`` to ``INSTALLED_APPS``
2. Define or replace ``AUTH_USER_MODEL`` with he new model, as below.
   
.. code:: python

    AUTH_USER_MODEL='improved_user.User'

3. In Django > 1.9, change ``UserAttributeSimilarityValidator`` to match
   correct ``User`` fields, as shown below.

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

Testing
-------

From the root directory of the project, run the code below.

.. code:: console

    $ python runtests.py
