Read Me
=======

This project provides a custom user model that improves on Django's
default by making a few modern and international changes.

* Uses email as the username to simplify login for users
* Replace ``first_name`` and ``last_name`` with international friendly
  ``short_name`` ``full name`` fields

Installation
------------

In a Terminal, use `pip` to install the package from
[PyPI](https://pypi.org/).

.. code:: console

    pip install django-improved-user

If you intend to use the `UserFactory` provided by the package to allow
for testing with [factory_boy](https://github.com/FactoryBoy/factory_boy),
you can specify so during install.

.. code:: console

    pip install django-improved-user[factory]

If you do not but wish to use the `UserFactory`, you will need to
install [factory_boy](https://github.com/FactoryBoy/factory_boy)
yourself.

Usage
-----

Perform the following steps in your ``settings.py`` file.

1. Add ``improved_user.apps.ImprovedUserConfig``
   (or simply ``improved_user``) to ``INSTALLED_APPS``
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

To run the test suite on a single version of Django (assuming you have a
version of Django installed), run the `runtests.py` script from the root
of the project.

.. code:: console

    $ python runtests.py

You can limit the tests or pass paramaters as if you had called
`manage.py test`.

.. code:: console

    $ ./runtests.py tests.test_basic -v 3

To run all linters and test multiple Python and Django versions, use
`tox`.

.. code:: console

    $ tox

You will need to install Python 3.4, 3.5, and 3.6 on your system for
this to work.
