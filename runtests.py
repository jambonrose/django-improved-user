#!/usr/bin/env python3
"""Utility script to setup Django and run tests against package"""
import sys
from os.path import dirname, join

from django import VERSION as DjangoVersion, setup
from django.conf import settings
from django.core.management import execute_from_command_line

try:
    import improved_user  # noqa: F401 pylint: disable=unused-import
except ImportError:
    print(
        'Could not load improved_user!\n'
        'Try running `./setup.py develop` before `./runtests.py`\n'
        'or run `./setup.py test` for an all in one solution',
    )
    exit(-1)


def run_test_suite(*args):
    """Heart of script: setup Django, run tests based on args"""
    test_args = list(args) or []

    middleware = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]

    if DjangoVersion >= (1, 10):
        middleware_var_name = 'MIDDLEWARE'
    else:
        middleware_var_name = 'MIDDLEWARE_CLASSES'

    middleware_kwargs = {
        middleware_var_name: middleware,
    }

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'improved_user.apps.ImprovedUserConfig',
        ],
        SITE_ID=1,
        AUTH_USER_MODEL='improved_user.User',
        FIXTURE_DIRS=(join(dirname(__file__), 'tests', 'fixtures'),),
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        # TODO: when Dj1.8 dropped, use MIDDLEWARE directly
        **middleware_kwargs  # noqa: C815
    )
    setup()
    execute_from_command_line(['manage.py', 'test'] + test_args)


if __name__ == '__main__':
    run_test_suite(*sys.argv[1:])
