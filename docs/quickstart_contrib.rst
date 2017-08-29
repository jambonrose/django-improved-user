########################
Quickstart: Contributing
########################

First off, thanks for taking the time to contribute! ✨🎉

This document assumes that you have forked and cloned the repository,
and that you seek to work on the package locally. If you are unsure how
to do this, please see the :doc:`contributing` documentation.

To test the package, start by installing the current package locally.

.. code:: console

    $ python setup.py develop

To run the test suite on a single version of Django (assuming you have a
version of Django installed), run the ``runtests.py`` script from the
root of the project.

.. code:: console

    $ python runtests.py

You can limit the tests or pass paramaters as if you had called
``manage.py test``.

.. code:: console

    $ ./runtests.py tests.test_basic -v 3

If you have Python 3.4, 3.5, and 3.6 installed on your system, you may
use ``tox`` to run all linters and test the package with multiple Python and
Django versions

.. code:: console

    $ tox

You may also limit tests to specific environments or test suites with tox. For instance:

.. code:: console

    $ tox -e py36-django111-unit tests.test_basic
    $ tox -e py36-django111-integration user_integration.tests.TestViews.test_home

Any change to the code should first be discussed in an issue.

For any changes, please create a new branch, make your changes, and open
a pull request on github agains the ``development`` branch. Refer to the
issue you are fixing or building. To make review of the PR easier,
please commit small, targeted changes.  Multiple small commits with
clear commit messages make reviewing changes easier. Rebasing your
branch to help clean up your changes is encouraged. Please remember that
this is a volunteer-driven project; we will look at your PR as soon as
possible.
