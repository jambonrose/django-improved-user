###############################################
How To: Use the Django Admin with Improved User
###############################################

Django Improved User defines an admin panel for the
:py:class:`~improved_user.models.User` model provided by the package.

The admin panel is used automatically if you are integrating directly
with the package (see :doc:`select_configuration_method` for more
information about different uses, and :doc:`integration` for
instructions on direct integration).

If you are extending the User model with **no changes** (as shown in the
:doc:`quickstart`), you can simply import the existing admin panel and
use it in your own project.

.. literalinclude:: ../example_extension_project/user_extension/admin.py

As noted in the comment in the file above, this method is not desirable
in production contexts. Additionally, it will not work in the event you
are replacing existing fields (as shown in
:doc:`create_custom_user_with_mixins`).

When using the extension method on a real/production site, or when
replacing existing fields, you will need to build your own admin panel.
Django doesn't supply mechanisms for simple inheritance of other admin
panels, and the package maintainers don't know what fields you're using,
so it's impossible for us to provide an easily extendable or re-usable
admin panel in these scenarios. We encourage you to look at
:py:class:`~improved_user.admin.UserAdmin` for guidance (printed below
for your convenience).

.. literalinclude:: ../src/improved_user/admin.py

.. NOTE::
   To allow the class above to be imported in demo situations, the
   module is lacking a call to register the :code:`UserAdmin` class.
   When you create your own class, you will need code similar to the
   snippet below.

    .. code:: python

        from django.contrib import admin
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin.site.register(User, NewUserAdmin)
