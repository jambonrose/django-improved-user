############################################
How To: Use Improved User in Data Migrations
############################################

Creating users in :ref:`data migrations <django:data-migrations>` is
**discouraged** as doing so represents a potential **security risk**, as
passwords are stored in plaintext in the migration. However, doing so in
proof-of-concepts or in special cases may be necessary, and the steps
below will demonstrate how to create and remove new users in a Django
data migration.

The ``django-improved-user`` package intentionally disallows use of
:py:class:`~improved_user.models.UserManager` in data migrations (we
forgo the :django:ref:`use of model managers in migrations
<django:using-managers-in-migrations>`). The
:py:meth:`~improved_user.models.UserManager.create_user` and
:py:meth:`~improved_user.models.UserManager.create_superuser` methods
are thus both unavailable when using data migrations. Both of these
methods rely on :py:class:`~improved_user.models.User` model methods
which are unavailable in :ref:`django:historical-models`, so we could
not use them even if we wanted to (short of refactoring large parts of
code currently inherited by Django).

We therefore rely on the standard
:py:class:`~django:django.db.models.Manager`, and supplement the
password creation behavior.

In an existing Django project, you will start by creating a new and
empty migration file. Replace :code:`APP_NAME` in the command below with the
name of the app for which you wish to create a migration.

.. code:: console

    $ python manage.py makemigrations --empty --name=add_user APP_NAME

We start by importing the necessary tools

.. literalinclude:: ../example_project/user_integration/migrations/0001_add_user.py
    :lines: 1-3

We will use :py:class:`~django.db.migrations.operations.RunPython` to
run our code. :py:class:`~django.db.migrations.operations.RunPython`
expects two functions with specific parameters. Our first function
creates a new user.

.. literalinclude:: ../example_project/user_integration/migrations/0001_add_user.py
    :pyobject: add_user

**NB**: Due to the lack of :py:class:`~improved_user.models.UserManager` or
:py:class:`~improved_user.models.User` methods, the :code:`email` field
is not validated or normalized. What's more, the :code:`password` field
is not validated against the project's password validators. **It is up
to the developer coding the migration file to provide proper values.**

The second function is technically optional, but providing one makes our
lives easier and is considered best-practice. This function undoes the
first, and deletes the user we created.

.. literalinclude:: ../example_project/user_integration/migrations/0001_add_user.py
    :pyobject: remove_user

Finally, we use our migration functions via
:py:class:`~django.db.migrations.operations.RunPython` in a
:py:class:`django:django.db.migrations.Migration` subclass.  Please note
the *addition* of the dependency below. If your file already had a
dependency, please add the tuple below, but do not remove the existing
tuple(s).

.. literalinclude:: ../example_project/user_integration/migrations/0001_add_user.py
    :pyobject: Migration

The final migration file is printed in totality below.

.. literalinclude:: ../example_project/user_integration/migrations/0001_add_user.py
    :linenos:

You may wish to read more about :ref:`Django Data Migrations
<django:data-migrations>` and
:py:class:`~django.db.migrations.operations.RunPython`.
