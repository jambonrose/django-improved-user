=======
History
=======

Next Release
------------

- Nothing yet!

0.4.0 (2017-08-14)
------------------

**Warning**: This is a **breaking change**, and migrations will conflict
with v0.3.0 due to PR `#23`_

- Add UserFactory to make testing easier for developers using the
  pacakge; requires factory_boy (PR `#20`_)
- Split the ``ImprovedIdentityMixin`` class into atomic parts:
  ``DjangoIntegrationMixin``, ``FullNameMixin``, ``ShortNameMixin``,
  ``EmailAuthMixin``.  This allows developers to create their own custom
  AbstractUsers if needed. (PR `#22`_)
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
  (PR `#18`)
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
