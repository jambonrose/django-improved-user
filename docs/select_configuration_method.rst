###############################################
Select a Configuration Method for Improved User
###############################################

The goal of this package is to improve your project's User model. To
that end, Improved User may be used in three different ways. You may:

1. inherit :py:class:`~improved_user.model_mixins.AbstractUser`
   in your own :code:`User` model (**extension**);
2. use the supplied :py:class:`~improved_user.models.User` model
   directly (**integration**);
3. create your own User model using the supplied model mix-in classes
   (**replacement**).

.. TIP::
    It is generally considered a good idea to change the :code:`User`
    model as infrequently and as little as possible, given the
    possibility of security problems. Creating a :code:`Profile`
    model---which has a foreign key to the :code:`User` model---to store
    your users' information can help avoid changes to the :code:`User`
    model.

****************
Extension Method
****************

The extension method is the recommended method to use when configuring
Improved User. Instructions for this method are found in
:doc:`quickstart`. This method gives the developer the most control and
flexibility, at the cost of having slightly extra code. This method is
the least likely to cause you problems in the long run, as it grants you
control of the model fields and migrations for your :code:`User` model,
and gives you the opportunity of entirely removing Improved User in the
future if you need to.

******************
Integration Method
******************

The integration option is the simplest, and uses the least code.
However, it is also the least flexible, as it assumes that you will
never change the structure of the :class:`~improved_user.models.User`
model. While this method may work fine for many, the amount of work
required to deal with any potential future change is very high. In many
ways, it is the most similar to Django's own
:class:`~.django.contrib.auth.models.User`: you gain all of the benefits
of the class directly, but forgo the ability to control or remove the
model in the future without serious work. You may refer to
:doc:`integration` to use this method.

.. WARNING::
    It will always be possible to switch between the extension and
    replacement methods, but is difficult to migrate to or from the
    integration method.

******************
Replacement Method
******************

The replacement method comes with the same trade-offs as the extension
method, but should be used in the event any of the fields included in
the :py:class:`~improved_user.model_mixins.AbstractUser` are not
desired. We recommend this method only to those very familiar with
Django. For more information, please refer to
:doc:`create_custom_user_with_mixins`.

