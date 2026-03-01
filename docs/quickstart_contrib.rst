########################
Quickstart: Contributing
########################

First off, thanks for taking the time to contribute! ✨🎉

This document assumes that you have forked and cloned the repository to
work on the package locally. If you are unsure how to do this, please
see the :doc:`contributing` documentation.

To test the package, start by installing it locally.

.. code:: console

    $ uv sync

To run the test suite on a single version of Django, run the
``runtests.py`` script from the root of the project.

.. code:: console

    $ uv run python runtests.py

You can limit tests or pass paramaters as when using ``manage.py test``.

.. code:: console

    $ uv run ./runtests.py tests.test_basic -v 3

If you have all of the supported Python versions installed,
you may use ``nox`` to run all linters and test the
package with multiple versions of Python and Django.

.. code:: console

    $ uv run nox

You may also limit tests to specific sessions or test suites with
nox. For instance:

.. code:: console

    $ uv run nox -s "unit(python='3.11', django='4.2')" -- tests.test_basic
    $ uv run nox -s "extension(python='3.12', django='4.2')"

Any change to the code should first be discussed in an issue.

For any changes, please create a new branch, make your changes, and open
a pull request on github agains the ``development`` branch. Refer to the
issue you are fixing or building. To make review of the PR easier,
please commit small, targeted changes.  Multiple small commits with
clear messages make reviewing changes easier. Rebasing your
branch to help clean up your changes is encouraged. Please remember that
this is a volunteer-driven project; we will look at your PR as soon as
possible.
