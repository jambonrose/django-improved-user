"""Test Improved User against Django's default backend"""
# pylint: disable=protected-access
from unittest.mock import patch

from django import VERSION as DjangoVersion
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, modify_settings, override_settings

from improved_user.models import User


class CountingMD5PasswordHasher(MD5PasswordHasher):
    """Hasher that counts how many times it computes a hash."""

    calls = 0

    def encode(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Add counter and call superclass to actually hash"""
        type(self).calls += 1
        return super().encode(*args, **kwargs)


class ImprovedUserModelBackendTest(TestCase):
    """
    Tests for the ModelBackend using the Improved User model.

    Looks for problems that may arise because auth.User
    is missing from db.

    The specific problem is queries on .filter(groups__user) et al,
    which makes an implicit assumption that the user model is called
    'User'. In production, the auth.User table won't exist, so the
    requested join won't exist either; in testing, the auth.User *does*
    exist, and so does the join. However, the join table won't contain
    any useful data; for testing, we check that the data we expect
    actually does exist.
    """

    UserModel = User
    backend = 'django.contrib.auth.backends.ModelBackend'

    def create_users(self):
        """Test utility to create users"""
        self.user = User._default_manager.create_user(
            email='test@example.com',
            password='test',
        )
        self.superuser = User._default_manager.create_superuser(
            email='test2@example.com',
            password='test',
        )

    def test_authenticate(self):
        """Additional test to ensure authentication"""
        authenticated_user = authenticate(
            email='test@example.com', password='test')
        self.assertEqual(self.user, authenticated_user)

    # Code below this point is from Django's BaseModelBackend superclass

    def setUp(self):
        """Add the backend to current settings"""
        self.patched_settings = modify_settings(
            AUTHENTICATION_BACKENDS={'append': self.backend},
        )
        self.patched_settings.enable()
        self.create_users()

    def tearDown(self):
        """Remove patched settings and flush cache"""
        self.patched_settings.disable()
        # The custom_perms test messes with ContentTypes, which will
        # be cached; flush the cache to ensure there are no side effects
        # Refs #14975, #14925
        ContentType.objects.clear_cache()

    def test_has_perm(self):
        """Refresh the user model to test permissions"""
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.assertIs(user.has_perm('auth.test'), False)

        user.is_staff = True
        user.save()
        self.assertIs(user.has_perm('auth.test'), False)

        user.is_superuser = True
        user.save()
        self.assertIs(user.has_perm('auth.test'), True)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = False
        user.save()
        self.assertIs(user.has_perm('auth.test'), False)

    def test_custom_perms(self):
        """Check interactions with custom permissions and groups"""
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        content_type = ContentType.objects.get_for_model(Group)
        perm = Permission.objects.create(
            name='test', content_type=content_type, codename='test')
        user.user_permissions.add(perm)

        # reloading user to purge the _perm_cache
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.assertEqual(user.get_all_permissions(), {'auth.test'})
        self.assertEqual(user.get_group_permissions(), set())
        self.assertIs(user.has_module_perms('Group'), False)
        self.assertIs(user.has_module_perms('auth'), True)

        perm = Permission.objects.create(
            name='test2', content_type=content_type, codename='test2')
        user.user_permissions.add(perm)
        perm = Permission.objects.create(
            name='test3', content_type=content_type, codename='test3')
        user.user_permissions.add(perm)
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.assertEqual(
            user.get_all_permissions(),
            {'auth.test2', 'auth.test', 'auth.test3'})
        self.assertIs(user.has_perm('test'), False)
        self.assertIs(user.has_perm('auth.test'), True)
        self.assertIs(user.has_perms(['auth.test2', 'auth.test3']), True)

        perm = Permission.objects.create(
            name='test_group',
            content_type=content_type,
            codename='test_group')
        group = Group.objects.create(name='test_group')
        group.permissions.add(perm)
        user.groups.add(group)
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        exp = {'auth.test2', 'auth.test', 'auth.test3', 'auth.test_group'}
        self.assertEqual(user.get_all_permissions(), exp)
        self.assertEqual(user.get_group_permissions(), {'auth.test_group'})
        self.assertIs(user.has_perms(['auth.test3', 'auth.test_group']), True)

        user = AnonymousUser()
        self.assertIs(user.has_perm('test'), False)
        self.assertIs(user.has_perms(['auth.test2', 'auth.test3']), False)

    def test_has_no_object_perm(self):
        """Verify proper return of perm object check

        Regression test for #12462
        https://code.djangoproject.com/ticket/12462

        """
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        content_type = ContentType.objects.get_for_model(Group)
        perm = Permission.objects.create(
            name='test', content_type=content_type, codename='test')
        user.user_permissions.add(perm)

        self.assertIs(user.has_perm('auth.test', 'object'), False)
        self.assertEqual(user.get_all_permissions('object'), set())
        self.assertIs(user.has_perm('auth.test'), True)
        self.assertEqual(user.get_all_permissions(), {'auth.test'})

    def test_anonymous_has_no_permissions(self):
        """Anonymous users shouldn't have permissions in ModelBackend

        #17903 -- Anonymous users shouldn't have permissions in
        ModelBackend.get_(all|user|group)_permissions().

        https://code.djangoproject.com/ticket/17903
        """
        backend = ModelBackend()

        user = self.UserModel._default_manager.get(pk=self.user.pk)
        content_type = ContentType.objects.get_for_model(Group)
        user_perm = Permission.objects.create(
            name='test', content_type=content_type, codename='test_user')
        group_perm = Permission.objects.create(
            name='test2', content_type=content_type, codename='test_group')
        user.user_permissions.add(user_perm)

        group = Group.objects.create(name='test_group')
        user.groups.add(group)
        group.permissions.add(group_perm)

        self.assertEqual(
            backend.get_all_permissions(user),
            {'auth.test_user', 'auth.test_group'})
        # Django 2.0 avoids cache permission problems
        # https://code.djangoproject.com/ticket/28713
        # https://github.com/django/django/pull/9242
        if DjangoVersion >= (2, 0):
            self.assertEqual(
                backend.get_user_permissions(user),
                {'auth.test_user'})
        else:
            self.assertEqual(
                backend.get_user_permissions(user),
                {'auth.test_user', 'auth.test_group'})
        self.assertEqual(
            backend.get_group_permissions(user),
            {'auth.test_group'})

        # In Django 1.10, is_anonymous became a property.
        if DjangoVersion >= (1, 10):
            is_anon_mock = True
        else:
            is_anon_mock = lambda s: True  # noqa: E731
        with patch.object(self.UserModel, 'is_anonymous', is_anon_mock):
            self.assertEqual(backend.get_all_permissions(user), set())
            self.assertEqual(backend.get_user_permissions(user), set())
            self.assertEqual(backend.get_group_permissions(user), set())

    def test_inactive_has_no_permissions(self):
        """Inactive users shouldn't have permissions in ModelBackend

        #17903 -- Inactive users shouldn't have permissions in
        ModelBackend.get_(all|user|group)_permissions().

        https://code.djangoproject.com/ticket/17903
        """
        backend = ModelBackend()

        user = self.UserModel._default_manager.get(pk=self.user.pk)
        content_type = ContentType.objects.get_for_model(Group)
        user_perm = Permission.objects.create(
            name='test', content_type=content_type, codename='test_user')
        group_perm = Permission.objects.create(
            name='test2', content_type=content_type, codename='test_group')
        user.user_permissions.add(user_perm)

        group = Group.objects.create(name='test_group')
        user.groups.add(group)
        group.permissions.add(group_perm)

        self.assertEqual(
            backend.get_all_permissions(user),
            {'auth.test_user', 'auth.test_group'})
        # Django 2.0 avoids cache permission problems
        # https://code.djangoproject.com/ticket/28713
        # https://github.com/django/django/pull/9242
        if DjangoVersion >= (2, 0):
            self.assertEqual(
                backend.get_user_permissions(user),
                {'auth.test_user'})
        else:
            self.assertEqual(
                backend.get_user_permissions(user),
                {'auth.test_user', 'auth.test_group'})
        self.assertEqual(
            backend.get_group_permissions(user),
            {'auth.test_group'})

        user.is_active = False
        user.save()

        self.assertEqual(backend.get_all_permissions(user), set())
        self.assertEqual(backend.get_user_permissions(user), set())
        self.assertEqual(backend.get_group_permissions(user), set())

    def test_get_all_superuser_permissions(self):
        """A superuser has all permissions.

        Refs #14795.
        https://code.djangoproject.com/ticket/14795

        """
        user = self.UserModel._default_manager.get(pk=self.superuser.pk)
        self.assertEqual(
            len(user.get_all_permissions()),
            len(Permission.objects.all()))

    @override_settings(
        PASSWORD_HASHERS=[
            'tests.test_auth_backends.CountingMD5PasswordHasher'])
    def test_authentication_timing(self):
        """Hasher is run once regardless of whether the user exists.

        Refs #20760.
        https://code.djangoproject.com/ticket/20760

        """
        # Re-set the password, because this tests overrides PASSWORD_HASHERS
        self.user.set_password('test')
        self.user.save()

        CountingMD5PasswordHasher.calls = 0
        username = getattr(self.user, self.UserModel.USERNAME_FIELD)
        authenticate(username=username, password='test')
        self.assertEqual(CountingMD5PasswordHasher.calls, 1)

        CountingMD5PasswordHasher.calls = 0
        authenticate(username='no_such_user', password='test')
        self.assertEqual(CountingMD5PasswordHasher.calls, 1)
