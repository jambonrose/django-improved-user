========================================
How To: Integrate Improved User Directly
========================================

.. WARNING::
    This configuration method is but one of three, and may not make the
    most sense for your project. Please read
    :doc:`select_configuration_method` before continuing, or else follow
    the instructions in :doc:`quickstart`.

In a new Django project, perform the following steps in the
``settings.py`` file or base settings file.

1. Add :code:`improved_user.apps.ImprovedUserConfig`
   to :code:`INSTALLED_APPS`

2. Define or replace :code:`AUTH_USER_MODEL` with the new model, as
   below.

    .. code:: python

        AUTH_USER_MODEL='improved_user.User'

3. Change :code:`UserAttributeSimilarityValidator` to match correct
   :code:`User` fields, as shown below.

    .. code:: python

        AUTH_PREFIX = 'django.contrib.auth.password_validation.'
        AUTH_PASSWORD_VALIDATORS = [
            {
                'NAME': AUTH_PREFIX + 'UserAttributeSimilarityValidator',
                'OPTIONS': {
                    'user_attributes': ('email', 'full_name', 'short_name')
                },
            },
            # include other password validators here
        ]

.. NOTE::
    Improved user also comes with forms, test factories, and an admin panel.
    Take a look at the :doc:`source/modules` for more information.
