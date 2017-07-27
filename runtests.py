import django
from django.conf import settings
from django.core.management import execute_from_command_line


def run_test_suite():
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
    )

    django.setup()

    execute_from_command_line(['manage.py', 'test'])


if __name__ == "__main__":
    run_test_suite()
