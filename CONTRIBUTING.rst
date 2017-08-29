=================
How to Contribute
=================

First off, thanks for taking the time to contribute! ✨🎉

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. The following is a
set of guidelines for contributing to django-improved-user, hosted on
`Github`_. These are mostly guidelines, not rules. Use your best
judgment, and feel free to propose changes to this document in a pull
request.

Please remember that this is a volunteer-driven project. We will look at
the issues and pull requests as soon as possible.

.. contents::
   :local:

Code of Conduct
---------------

This project is subject to a `Code of Conduct`_. By participating, you
are expected to uphold this code.

Please be respectful to other developers.

.. _Code of Conduct: https://github.com/jambonsw/django-improved-user/blob/development/CODE_OF_CONDUCT.md

Types of Contributions
----------------------

You can contribute in many ways:

Report Bugs
~~~~~~~~~~~

Please report bugs on the `Github issue tracker`_. Search the tracker to
make sure someone else hasn't already reported the issue. If you find
your the problem has already been reported, feel free to add more
information if appropriate.  If you don't find the problem reported,
please open a new issue, and follow the guidelines set forth in the text
field.

Fix Bugs
~~~~~~~~

Look through the `Github issue tracker`_ for bugs. Anything tagged with
"bug" and "help wanted" is open to whoever wants to implement it. If
someone has been assigned, or notes that it is claimed in the comments,
please reach out to them to work together on the issue to avoid
duplicating work. Note that, as volunteers, people sometime are unable
to complete work they start, and that it is reasonable after a certain
amount of time to assume they are no longer working on the issue. Use
your best judgment to assess the situation.

Write (or Request) Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation aims to provide reference material, how-to guides, and
a general tutorial for getting started with Django and
django-improved-user. If you believe the documentation can be expanded
or added to, your contribution would be welcomed.

If you are running into a problem, and believe that some documentation
could clarify the problem (or the solution!) please feel free to request
documentation on the `Github issue tracker`_.

For more about different kinds of documentations and how to think about
the differences, please watch `Daniele Procida's PyCon US 2017 talk`_ on
the subject.

.. _Daniele Procida's PyCon US 2017 talk: https://www.youtube.com/watch?v=azf6yzuJt54

Your First Contribution
----------------------------

Ready to contribute? Let's get django-improved-user working on your
local machine.

This package relies on Python, pip, and Django. Please make sure you
have the first two installed.

To get started, fork the git repository to your own account using the
fork button on the top right of the Github interface. You now have your
own fork of the project! Clone your fork of the repository using the
command below, but with your own username.

.. code:: console

    $ git clone git@github.com:YOUR_USERNAME/django-improved-user.git

We recommend the use of virtual environments when developing
(generally). If you are not familiar with virtual environments, take a
look at `Python's venv documentation`_. `Virtualenvwrapper`_ is also a
favorite.

.. _Python's venv documentation: https://docs.python.org/3/library/venv.html#module-venv
.. _Virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/

You can now install all of the dependencies required to develop the
project.  Use pip to install all dependencies, as demonstrated below.

.. code:: console

    $ pip install -r requirements.txt

If you are modifying code, keep reading. If you are changing
documentation, skip to the next section.

Your First Code Contribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before making any changes, let's first make sure all the tests pass.  To
run the test suite on a single version of Django, you will need to
install Django and the package (in development mode). Use the command
below to do both.

.. code:: console

    $ python setup.py develop

Run the `runtests.py` script from the root of the project to test the
django-improved-user project.

.. code:: console

    $ python runtests.py

You can limit the tests or pass paramaters as if you had called Django's
`manage.py test`.

.. code:: console

    $ ./runtests.py tests.test_basic -v 3

If you have Python 3.4, 3.5, and 3.6 installed on your system, you will
be able to test the package under all required conditions. The project
uses `tox` to make this easy. This will use all the linters and test the
package with multiple Python and Django versions.

.. code:: console

    $ tox

Note that any change made to this project must meet the linting rules
and tests run by tox. These rules are double-checked by TravisCI and
AppVeyor. Furthermore, changes in code must maintain or increase
code-coverage unless this is unreasonable.

If your tests all pass, you are ready to make changes! If not, please
open an issue in Github detailing the test failure you are seeing.

Create a new branch in the repository. Name the branch descriptively,
and reference the the github issue if applicable. Below are a few
examples of what that command might look like.

.. code:: console

    $ git checkout -b add_how_to_subclass_abstract_user_guide
    $ git checkout -b issue_45_allow_whitespace_in_passwords

Please note that all pull requests that feature code changes are
expected to reference github issues, as discussion is required for any
change.

Make your changes! We recommend a test-driven approach to development.
Please remember to update any relevant documentation. Make your commits
small, and target each commit to do a single thing. If you are
comfortable rebasing git commits, please do so at the end - providing
small, targeted, organized commits can make reviewing code radically
easier, and we will be grateful for it.

Once you are done, push your changes to github, and open a pull request
via the interface. Please follow all of the instructions in the pull
request textfield when doing so, as it will help us understand and
review your code.

Congratulations on opening a pull request! 🎉

Your First Documentation Contribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    If it isn't documented, it doesn't exist.

    — `Mike Pope`_

.. _Mike Pope: http://www.mikepope.com/blog/DisplayBlog.aspx?permalink=1680

Documentation is crucial, and I am thrilled to get your help writing it!

All of the documentation is written in `reStructuredText`_, sometimes
called *rst*. Some of the documents (such as this one!) are in the root
of the `Github`_ project, but the vast majority exist in the ``docs``
directory. The documents found in this directory are compiled to HTML by
`Sphinx`_ (which has a `primer on rst`_).

You may use the ``Makefile`` in the ``docs`` directory to run Sphinx.

.. code:: console

    $ cd docs
    $ make clean && make html

If you browse to ``_build/html`` (within the ``docs`` directory), you'll
find a local build of all the documentation! Open any of the HTML files
in a browser to read the documentation.

Alternatively, you can use ``tox`` to build the documentation (requires
that Python 3.6 be installed). This is more of a check, as navigating to
the built files is less easy.

.. code:: console

    $ tox -e docs

The documentation automatically builds reference documentation for the
project. To update these reference documents, you will need to change
the Python docstrings in the code itself. Corrections and expansions to
existing docs, as well as new tutorials and how-to guides are welcome
additions. If you had a pain point while using this project, and you
would like to add to an existing document or else to write a new one,
you are encouraged to do it!

If you run into an problems or have a question, please ask it on the
`Github issue tracker`_ (after making sure someone hasn't already asked
and answered the question!).

Once you have made changes to the documents in question, you'll want to
make sure that Sphinx builds the documentation without any errors.

Commit your changes, and push them to your local branch. Using the
Github interface, open a pull request to the development branch in the
main repository!  Please follow all of the instructions in the pull
request textfield when doing so, as it will help us understand and
review your code.

Congratulations on opening a pull request! 🎉

.. _Github issue tracker: https://github.com/jambonsw/django-improved-user/issues
.. _Github: https://github.com/jambonsw/django-improved-user
.. _primer on rst: http://www.sphinx-doc.org/en/stable/rest.html#rst-primer
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://www.sphinx-doc.org/
