#!/usr/bin/env python3
import sys
from os.path import dirname, join

from django import setup
from django.conf import settings
from django.core.management import execute_from_command_line


def run_test_suite(*args):
    test_args = args or []

    settings.configure(
        DATABASES={
            "default": {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "improved_user",
        ],
        AUTH_USER_MODEL='improved_user.User',
        FIXTURE_DIRS=(join(dirname(__file__), 'tests', 'fixtures'),),
    )
    setup()
    execute_from_command_line(['manage.py', 'test', *test_args])


if __name__ == "__main__":
    run_test_suite(*sys.argv[1:])
