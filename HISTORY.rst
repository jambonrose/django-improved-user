=======
History
=======

Next Release
------------

- Nothing Yet!

1.0.1 (2020-02-16)
------------------

- Add flexibility to admin panel usage; document usage

1.0.0 (2018-07-28)
------------------

- Django 1.8, 1.11, 2.0, 2.1 officially supported.
- Django 1.9 and 1.10 are not tested against, as Django does not support
  them, but they likely work.
- **Breaking change**: Model mix-in classes now exist in their own
  module! Import from `model_mixins` instead of `models`. (`#46`_,
  `#96`_)
- Fix issue `#49`_: allow form classes to be imported without requiring
  project to be in ``INSTALLED_APPS`` (See `#36`_ and `#46`_ below for
  associated error and reasoning) (`#50`_)
- Fix issue `#36`_: refactor package to allow for mix-in classes to be
  imported into third-party project without requiring project to be in
  ``INSTALLED_APPS`` (which would unnecessarily create unused tables in
  the project). Add documentation/tutorial on subject. (`#46`_)
- Django 2.0, 2.1 compatibility. (`#43`_, `#93`_)

.. _#36: https://github.com/jambonsw/django-improved-user/issues/36
.. _#43: https://github.com/jambonsw/django-improved-user/pull/43
.. _#46: https://github.com/jambonsw/django-improved-user/pull/46
.. _#49: https://github.com/jambonsw/django-improved-user/issues/49
.. _#50: https://github.com/jambonsw/django-improved-user/pull/50
.. _#93: https://github.com/jambonsw/django-improved-user/pull/93
.. _#96: https://github.com/jambonsw/django-improved-user/pull/96


0.5.3 (2017-08-29)
------------------

- Include history of changes in online documentation. (`#34`_)
- Write documentation about why and how the project was built. (`#34`_)
- Add section about contributing documentation. (`#34`_)

.. _#34: https://github.com/jambonsw/django-improved-user/pull/34

0.5.2 (2017-08-27)
------------------

- Change `package PyPI`_ license identifier for better information on
  `djangopackages.org detail page`_. See
  `djangopackages/djangopackages#483`_ for more information.

.. _package PyPI: https://pypi.org/project/django-improved-user/
.. _djangopackages.org detail page: https://djangopackages.org/packages/p/django-improved-user/
.. _djangopackages/djangopackages#483: https://github.com/djangopackages/djangopackages/issues/483

0.5.1 (2017-08-27)
------------------

- Docfix: Remove links to ReadTheDocs Stable version from ReadMe, as we
  are unable to build that version until v1.0.0 release. See
  `rtfd/readthedocs.org#2032`_ for more information. (`#31`_)

.. _rtfd/readthedocs.org#2032: https://github.com/rtfd/readthedocs.org/issues/2032
.. _#31: https://github.com/jambonsw/django-improved-user/pull/31

0.5.0 (2017-08-26)
------------------

- Provide documentation for the package. This includes Sphinx
  documentation hosted on ReadTheDocs.org, (`#26`_, `#29`_), but also
  documents to help contribute to github more easily (`#26`_) as well as
  a code of conduct (`#26`_). The Read Me includes badges (`#26`_).
- In the event the documentation isn't enough, the project now includes
  an example project demonstrating integration of django-improved-user
  with Django as well as django-registration. (`#28`_) This content is
  used to create some of the documentation (`#29`_).
- Bugfix: The ``UserManager`` was setting the ``last_login`` attribute
  of new users at creation time. Reported in `#25`_, fixed in `#27`_
  (``last_login`` is ``None`` until the user actually logs in).

.. _#25: https://github.com/jambonsw/django-improved-user/issues/25
.. _#26: https://github.com/jambonsw/django-improved-user/pull/26
.. _#27: https://github.com/jambonsw/django-improved-user/pull/27
.. _#28: https://github.com/jambonsw/django-improved-user/pull/28
.. _#29: https://github.com/jambonsw/django-improved-user/pull/29

0.4.0 (2017-08-14)
------------------

**Warning**: This is a **breaking change**, and migrations will conflict
with v0.3.0 due to PR `#23`_

- Add ``UserFactory`` to make testing easier for developers using the
  package; requires factory_boy (PR `#20`_)
- Split the ``ImprovedIdentityMixin`` class into atomic parts:
  ``DjangoIntegrationMixin``, ``FullNameMixin``, ``ShortNameMixin``,
  ``EmailAuthMixin``.  This allows developers to create their own custom
  ``AbstractUsers`` if needed. (PR `#22`_)
- Change ``blank`` to ``True`` on ``short_name`` field of User model.
  (**Breaking change!** PR `#23`_).

.. _#20: https://github.com/jambonsw/django-improved-user/pull/20
.. _#22: https://github.com/jambonsw/django-improved-user/pull/22
.. _#23: https://github.com/jambonsw/django-improved-user/pull/23

0.3.0 (2017-08-10)
------------------

- Integrate coverage and codecov service (PR `#16`_)
- Make TravisCI test builds public (first seen in PR `#16`_)
- Merge appropriate tests from Django master (1.11.3 is current release
  at time of writing). This increases test coverage across the board and
  updates the test suite to check for parity between Django's User API
  and Improved User's API as well as check for the same security issues.
  (PR `#18`_)
- UserManager raises a friendly error if the developer tries to pass a
  username argument (PR `#18`_)
- Password errors are shown above both password fields
  (PR `#18`_)
- Bugfix: UserManager handles is_staff, is_active, and is_superuser
  correctly (PR `#18`_)
- Bugfix: User has email normalized during Model.clean phase (PR `#18`_)
- Bugfix: UserAdmin requires short_name in both add and change
  (previously only in change; PR `#18`_)
- Bugfix: UserAdmin uses correct relative path URL for password change
  in all versions of Django (was not working in Django 1.9+) (PR `#18`_)
- Bugfix: Runtests correctly handles test specification (PR `#18`_)

.. _#16: https://github.com/jambonsw/django-improved-user/pull/16
.. _#18: https://github.com/jambonsw/django-improved-user/pull/18

0.2.0 (2017-07-30)
------------------

- Reorganize project to follow best practices (PR `#9`_)
- Allow setup.py to run tests by overriding test command (PR `#9`_)
- Test locally with Tox (PR `#10`_)
- Remove Django 1.9 from supported versions (PR `#10`_)
- Enforce styleguide with flake8, isort, and pylint.
  Use flake8-commas and flake8-quotes to enhance flake8.
  Override default distutils check command to check package metadata.
  Use check-manifest to check contents of MANIFEST.in (PR `#11`_)
- Integrate https://pyup.io/ into project (PR `#12`_)
- Upgrade flake8 to version 3.4.1 (PR `#13`_)
- Make release and distribution less painful with
  bumpversion package and a Makefile (PR `#15`_)
- Add HISTORY.rst file to provide change log (PR `#15`_)

.. _#9: https://github.com/jambonsw/django-improved-user/pull/9
.. _#10: https://github.com/jambonsw/django-improved-user/pull/10
.. _#11: https://github.com/jambonsw/django-improved-user/pull/11
.. _#12: https://github.com/jambonsw/django-improved-user/pull/12
.. _#13: https://github.com/jambonsw/django-improved-user/pull/13
.. _#15: https://github.com/jambonsw/django-improved-user/pull/15

0.1.1 (2017-06-28)
------------------

- Fix metadata in setup.py for warehouse
  (see https://github.com/pypa/warehouse/issues/2155 and PR `#8`_)

.. _#8: https://github.com/jambonsw/django-improved-user/pull/8

0.1.0 (2017-06-28)
------------------

- Add tests for Django 1.11 (PR `#5`_)
- Allow for integration with UserAttributeSimilarityValidator
  (see https://code.djangoproject.com/ticket/28127,
  https://github.com/django/django/pull/8408, and PR `#5`_)
- Rename project django-improved-user (from django-simple-user)
- Make development default branch (PR `#6`_)
- Initial public release (PR `#7`_)
- Use Simplified BSD License instead of Revised BSD License (`#7`_)

.. _#5: https://github.com/jambonsw/django-improved-user/pull/5
.. _#6: https://github.com/jambonsw/django-improved-user/pull/6
.. _#7: https://github.com/jambonsw/django-improved-user/pull/7

0.0.1 (2016-10-26)
------------------

- Simplified User model for better international handling.
  Includes forms and admin configuration (PR `#1`_)
- All tests run on TravisCI (PR `#3`_)
- Compatible with:
    - Python 3.4, 3.5, 3.6
    - Django 1.8 through 1.10 (PR `#3`_ and `#4`_)

.. _#1: https://github.com/jambonsw/django-improved-user/pull/1
.. _#3: https://github.com/jambonsw/django-improved-user/pull/3
.. _#4: https://github.com/jambonsw/django-improved-user/pull/4
