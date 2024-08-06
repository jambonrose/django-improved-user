Latest Release: |Version| |Tag|

Documentation: |StableDocs|

Compatibility: |Python| |Django| |License| |Black|

Tests: |Pre-commit| |Coverage|

.. |Version| image:: https://img.shields.io/pypi/v/django-improved-user
		:target: https://pypi.org/project/django-improved-user/
		:alt: PyPI Version

.. |Tag| image:: https://img.shields.io/github/v/tag/jambonrose/django-improved-user
		:target: https://github.com/jambonrose/django-improved-user/releases
		:alt: Github Tag

.. |StableDocs| image:: https://readthedocs.org/projects/django-improved-user/badge/?version=stable
		:target: https://django-improved-user.readthedocs.io/en/stable/?badge=stable
		:alt: Stable Documentation Status

.. |Python| image:: https://img.shields.io/pypi/pyversions/django-improved-user
		:target: https://pypi.org/project/django-improved-user/
		:alt: Python Support

.. |Django| image:: https://img.shields.io/pypi/frameworkversions/django/django-improved-user
		:target: https://pypi.org/project/django-improved-user/
		:alt: Django Support

.. |License| image:: https://img.shields.io/pypi/l/django-improved-user
		:target: http://opensource.org/licenses/BSD-2-Clause
		:alt: License

.. |Pre-commit| image:: https://results.pre-commit.ci/badge/github/jambonrose/django-improved-user/development.svg
		:target: https://results.pre-commit.ci/latest/github/jambonrose/django-improved-user/development
		:alt: pre-commit.ci status

.. |Coverage| image:: https://codecov.io/gh/jambonrose/django-improved-user/branch/development/graph/badge.svg
		:target: https://codecov.io/gh/jambonrose/django-improved-user
		:alt: Coverage Status

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000
		:target: https://github.com/psf/black

.. end-badges

Read Me
=======

This project provides a custom user model that improves on Django's
default by making a few modern and international changes.

* Uses email as the username to simplify login for users
* Replace :code:`first_name` and :code:`last_name` with international
  friendly :code:`short_name` and :code:`full_name` fields

The project also provides mix-in classes to make building custom User
models easier.

For an explanation of why and how the project was built, please see the
`Project Rationale`_.

For information about getting started, please refer to the `quickstart
documentation`_.

For information about how to help with the project, please see the
`contributing documentation`_.

.. _contributing documentation: https://django-improved-user.readthedocs.io/en/latest/contributing.html
.. _Project Rationale: https://django-improved-user.readthedocs.io/en/latest/rationale.html
.. _quickstart documentation: https://django-improved-user.readthedocs.io/en/latest/quickstart.html
