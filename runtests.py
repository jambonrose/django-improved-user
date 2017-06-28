from os.path import abspath, dirname, join

import django
from django.conf import settings
from django.core.management import execute_from_command_line

TESTS_ROOT = abspath(dirname(dirname(__file__)))


def run_test_suite():
    settings.configure(
        DATABASES={
            "default": {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': join(TESTS_ROOT, 'db.sqlite3'),
                "USER": "",
                "PASSWORD": "",
                "HOST": "",
                "PORT": "",
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
    )

    django.setup()

    execute_from_command_line(['manage.py', 'test'])


if __name__ == "__main__":
    run_test_suite()
