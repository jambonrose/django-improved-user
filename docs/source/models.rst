###################
Improved User Model
###################

.. autoclass:: improved_user.models.User(email, password, short_name=None, full_name=None)
   :members: check_password, clean, email_user, get_full_name, get_short_name,
             get_username, has_module_perms, has_perm, has_perms,
             is_anonymous, is_authenticated, refresh_from_db
   :show-inheritance:
