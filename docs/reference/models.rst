#################
Reference: Models
#################

**********
User Model
**********

.. py:class:: improved_user.models.User(email, password, short_name=None, full_name=None)

    The Improved User model itself. Do not import this model directly.
    Instead, please use :py:func:`~django.contrib.auth.get_user_model`.

    .. py:attribute:: email

        Django EmailField. Required.

    .. py:attribute:: password

        Django CharField with max 128 chararcters. Required. 

    .. py:attribute:: short_name

        A string to use when addressing the user casually. Optional.

    .. py:attribute:: full_name

        A string to use when addressing the user formally. Optional.

    .. py:method:: get_short_name()

        Returns the user's
        :py:attr:`improved_user.models.User.short_name`

    .. py:method:: get_full_name()

        Returns the user's
        :py:attr:`improved_user.models.User.full_name`

**************
Mixin Classes
**************

These classes are provided as tools to help build your own User models.

.. autoclass:: improved_user.models.DjangoIntegrationMixin
   :members:
   :undoc-members:
