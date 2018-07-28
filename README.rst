Latest Release: |Version| |Tag|

Documentation: |DevelopmentDocs|

Compatibility: |Implementation| |Python| |Django| |License|

Tests: |Travis| |AppVeyor| |Coverage| |PyUp|

.. |Version| image:: http://img.shields.io/pypi/v/django-improved-user.svg
        :target: https://pypi.org/project/django-improved-user/
        :alt: PyPI Version

.. |Tag| image:: https://img.shields.io/github/tag/jambonsw/django-improved-user.svg
        :target: https://github.com/jambonsw/django-improved-user/releases
        :alt: Github Tag

.. .. |StableDocs| image:: https://readthedocs.org/projects/django-improved-user/badge/?version=stable
..         :target: http://django-improved-user.readthedocs.io/en/stable/?badge=stable
..         :alt: Stable Documentation Status

.. |DevelopmentDocs| image:: https://readthedocs.org/projects/django-improved-user/badge/?version=latest
        :target: http://django-improved-user.readthedocs.io/en/latest/?badge=latest
        :alt: Development Documentation Status

.. |Implementation| image:: https://img.shields.io/pypi/implementation/django-improved-user.svg
        :target: https://pypi.org/project/django-improved-user/
        :alt: Python Implementation Support

.. |Python| image:: https://img.shields.io/pypi/pyversions/django-improved-user.svg
        :target: https://pypi.org/project/django-improved-user/
        :alt: Python Support

.. |Django| image:: https://img.shields.io/badge/Django-1.8%2C%201.11%2C%202.0%2C%202.1-blue.svg
        :target: https://pypi.org/project/django-improved-user/
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
