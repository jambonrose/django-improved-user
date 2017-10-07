from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def add_user(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    User.objects.create(
        email='migrated@jambonsw.com',
        password=make_password('s3cr3tp4ssw0rd!'),
        short_name='Migrated',
        full_name='Migrated Improved User',
    )


def remove_user(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    User.objects.get(email='migrated@jambonsw.com').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('improved_user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user, remove_user),
    ]
