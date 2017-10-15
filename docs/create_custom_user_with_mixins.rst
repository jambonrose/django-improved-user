#########################################
How To: Create a Custom User using Mixins
#########################################

The :py:class:`~improved_user.models.User` supplied by the package is
not always what you want, and being able to flexibly create a custom
User model for specific use cases is important.  While extending the
model is a straightforward process, creating a new User model that does
not have fields found on the improved User is more difficult.  In this
tutorial, we will create a new custom User that has an email field and
password, but which does not feature either the ``short_name`` or
``full_name`` fields.

.. WARNING::
    Not supplying methods for names on the User model will cause
    problems with Django's Admin.

.. TIP::
    If you're looking to extend the
    :py:class:`~improved_user.models.User` model, rather than replace
    it as shown in this tutorial, use the following steps:

    1. inherit :py:class:`~improved_user.mixins.AbstractUser`
    2. add new fields as desired
    3. override
       :attr:`~django.contrib.auth.models.CustomUser.REQUIRED_FIELDS`
       if necessary (remembering to put ``'short_name',
       'full_name'`` in the list)

In an existing app, in the ``models.py`` file, we start by importing the
tools we need to build the model. We first import classes from Django.

.. literalinclude:: ../example_replacement_project/user_replacement/models.py
    :lines: 2-3

:py:class:`~django.contrib.auth.models.AbstractBaseUser` and
:py:class:`~django.contrib.auth.models.PermissionsMixin` will serve as a
base for the User (click the classes in this sentence to see Django's
official documentation on the subject). We also import
:py:func:`~django.utils.translation.ugettext_lazy` to enable translation
of our strings.

We then import mix-in classes from Improved User.

.. literalinclude:: ../example_replacement_project/user_replacement/models.py
    :lines: 5-6

The :py:class:`~improved_user.mixins.DjangoIntegrationMixin` class
provides fields that allow the model to integrate with Django's default
Authentication Backend as well as a field to allow for integration with
Django's Admin.

The :py:class:`~improved_user.mixins.EmailAuthMixin` creates an
:py:class:`~django.db.models.EmailField` and sets the field to be used
as the username during the authentication process.

The :py:class:`~improved_user.managers.UserManager` is a custom model
manager that provides the
:py:meth:`~improved_user.managers.UserManager.create_user` and
:py:meth:`~improved_user.managers.UserManager.create_superuser` methods
used in Django.

.. DANGER::
    Improved Users' custom
    :py:class:`~improved_user.managers.UserManager` is intended to work
    with subclasses of :py:class:`~improved_user.mixins.EmailAuthMixin`,
    and will likely not work with your User subclass if you are using a
    different field for your username. You will, in that case, need to
    create your own ``UserManager``. The source code for Improved Users'
    :py:class:`~improved_user.managers.UserManager` as well as Django's
    :py:class:`~django.contrib.auth.models.BaseUserManager` and
    :class:`~django.contrib.auth.models.UserManager` would likely prove
    helpful.

.. NOTE::
    If you wanted to create a User model with a field other than email
    for username, you would set the
    :attr:`~django.contrib.auth.models.CustomUser.USERNAME_FIELD` on
    your User model to the name of the field that should serve as the
    username.  Please take a look at the source of
    :py:class:`~improved_user.mixins.EmailAuthMixin` for an example of
    this.

With all our tools in place, we can now create a User model. We start by
creating a class that inherits all of the classes we have imported, and
then we tie the :py:class:`~improved_user.managers.UserManager` to the
new model.


.. literalinclude:: ../example_replacement_project/user_replacement/models.py
    :lines: 9-15

For good measure, we can specify the name and verbose name of the model,
making sure to internationalize the strings. Our full and final
``models.py`` file is shown below.

.. literalinclude:: ../example_replacement_project/user_replacement/models.py

.. TIP::
    Setting ``abstract = True`` in the ``Meta`` class would allow the
    class above to be an AbstractUser model similar to
    :py:class:`~improved_user.mixins.AbstractUser`
