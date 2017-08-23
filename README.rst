Latest Release: |Version| |Tag|

Compatibility: |Implementation| |Python| |Django| |License|

Tests: |Travis| |AppVeyor| |Coverage| |PyUp|

.. |Version| image:: http://img.shields.io/pypi/v/django-improved-user.svg
        :target: https://pypi.org/project/django-improved-user/
        :alt: PyPI Version

.. |Tag| image:: https://img.shields.io/github/tag/jambonsw/django-improved-user.svg
        :target: https://github.com/jambonsw/django-improved-user/releases
        :alt: Github Tag

.. |Implementation| image:: https://img.shields.io/pypi/implementation/django-improved-user.svg
        :target: https://pypi.python.org/pypi/django-improved-user/
        :alt: Python Implementation Support

.. |Python| image:: https://img.shields.io/pypi/pyversions/django-improved-user.svg
        :target: https://pypi.python.org/pypi/django-improved-user/
        :alt: Python Support

.. |Django| image:: https://img.shields.io/badge/Django-1.8%2C%201.10%2C%201.11-blue.svg
        :target: https://pypi.python.org/pypi/django-improved-user/
        :alt: Django Support

.. |License| image:: http://img.shields.io/pypi/l/django-improved-user.svg
        :target: http://opensource.org/licenses/BSD-2-Clause
        :alt: License

.. |Travis| image:: https://travis-ci.org/jambonsw/django-improved-user.svg?branch=development
        :target: https://travis-ci.org/jambonsw/django-improved-user
        :alt: Travis Build Status

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/mfbtcx2didsjpwo7/branch/development?svg=true
        :target: https://ci.appveyor.com/project/jambonrose/django-improved-user/branch/development
        :alt: AppVeyor Build Status

.. |Coverage| image:: https://codecov.io/gh/jambonsw/django-improved-user/branch/development/graph/badge.svg
        :target: https://codecov.io/gh/jambonsw/django-improved-user
        :alt: Coverage Status

.. |PyUp| image:: https://pyup.io/repos/github/jambonsw/django-improved-user/shield.svg
        :target: https://pyup.io/repos/github/jambonsw/django-improved-user/
        :alt: Updates

.. end-badges

Read Me
=======

This project provides a custom user model that improves on Django's
default by making a few modern and international changes.

* Uses email as the username to simplify login for users
* Replace :code:`first_name` and :code:`last_name` with international
  friendly :code:`short_name` and :code:`full_name` fields

Installation
------------

In a Terminal, use :code:`pip` to install the package from `PyPI`_.

.. code:: console

    pip install django-improved-user

If you intend to use the ``UserFactory`` provided by the package to
allow for testing with |factory_boy|_, you can specify so during
install.

.. code:: console

    pip install django-improved-user[factory]

If you do not but wish to use the :code:`UserFactory`, you will need to
install |factory_boy|_ yourself.

.. _PyPI: https://pypi.org
.. _factory_boy: https://github.com/FactoryBoy/factory_boy
.. |factory_boy| replace:: :code:`factory_boy`

Usage
-----

Perform the following steps in your ``settings.py`` file.

1. Add :code:`improved_user.apps.ImprovedUserConfig`
   (or simply :code:`improved_user`) to :code:`INSTALLED_APPS`
2. Define or replace :code:`AUTH_USER_MODEL` with he new model, as
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

Testing
-------

To run the test suite on a single version of Django (assuming you have a
version of Django installed), run the ``runtests.py`` script from the
root of the project.

.. code:: console

    $ python runtests.py

You can limit the tests or pass paramaters as if you had called
``manage.py test``.

.. code:: console

    $ ./runtests.py tests.test_basic -v 3

To run all linters and test multiple Python and Django versions, use
``tox``.

.. code:: console

    $ tox

You will need to install Python 3.4, 3.5, and 3.6 on your system for
this to work.

You may also limit tests to specific environments or test suites with tox. For instance:

.. code:: console

    $ tox -e py36-django111-unit tests.test_basic
    $ tox -e py36-django111-integration user_integration.tests.TestViews.test_home
