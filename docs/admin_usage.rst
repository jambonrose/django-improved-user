#########################################
Using the Django Admin with Improved User
#########################################

Django Improved User defines an admin panel for the
:py:class:`~improved_user.models.User` model provided by the package.

The admin panel is used automatically if you are integrating directly
with the package (see :doc:`select_configuration_method` for more
information about different uses, and :doc:`integration` for
instructions on direct integration).

If you are extending the User model with no changes (as shown in the
:doc:`quickstart`), you can simply import the existing admin panel and
use it in your own project.

If you are extending the User model with new fields, or replacing
existing fields (as shown in :doc:`create_custom_user_with_mixins`) then
you will need to build your own admin panel. Django doesn't supply
mechanisms for simple inheritance of other admin panels, and the package
maintainers don't know what fields you're using, so it's impossible for
us to provide an easily extendable or re-usable admin panel in these
scenarios. We encourage you to look at
:py:class:`~improved_user.admin.UserAdmin` for guidance, though.
