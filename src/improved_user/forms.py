"""Forms for Creating and Updating Improved Users"""
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import User

try:
    from django.contrib.auth import password_validation
except ImportError:
    class EmptyValidator:
        """
        Class to mimic password validator API

        Django 1.8 doesn't have password strength validation
        We therefore introduce a mimic into the namespace

        """
        def validate_password(self, password, instance):
            """Accept password and user model and do nothing"""
            pass

        # pylint: disable=no-self-use
        def password_validators_help_text_html(self):
            """
            Used by password1 field;
            return None, as all strings are valid passwords

            """
            return None

    password_validation = EmptyValidator()


class AbstractUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given
    username and password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'))

    def clean_password2(self):
        """Check wether password 1 and password 2 are equivalent"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        """
        Run password validaton after clean methods

        When clean methods are run, the user instance does not yet
        exist.  To properly compare model values agains the password (in
        the UserAttributeSimilarityValidator), we wait until we have an
        instance to compare against.

        https://code.djangoproject.com/ticket/28127
        https://github.com/django/django/pull/8408

        Has no effect in Django prior to 1.9
        May become unnecessary in Django 2.0 (if this superclass changes)

        """
        super()._post_clean()  # updates self.instance with form data
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        """Save the user; use password hasher to set password"""
        user = super(AbstractUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserCreationForm(AbstractUserCreationForm):
    """
    A concrete implementation of AbstractUserCreationForm that uses an
    e-mail address as a user's identifier.
    """
    # TODO: when Py3.4 dropped, replace comprehension below with:
    # error_messages = {
    #     **AbstractUserCreationForm.error_messages,
    #     'duplicate_email': _('A user with that email already exists.'),
    # }
    error_messages = {
        k: v
        for d in [
            AbstractUserCreationForm.error_messages,
            {'duplicate_email': _('A user with that email already exists.')}]
        for k, v in d.items()
    }

    class Meta:
        model = User
        fields = ('email', 'full_name', 'short_name')

    def clean_email(self):
        """
        Clean email; set nice error message

        Since User.email is unique, this check is redundant,
        but it sets a nicer error message than the ORM. See #13147.
        """
        email = self.cleaned_data['email']
        try:
            # https://docs.djangoproject.com/en/stable/topics/db/managers/#default-managers
            # pylint: disable=protected-access
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )


class AbstractUserChangeForm(forms.ModelForm):
    """Base form update User, but not their password"""
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_('Raw passwords are not stored, so there is no way to see '
                    "this user's password, but you can change the password "
                    'using <a href="password/">this form</a>.'))

    def __init__(self, *args, **kwargs):
        """Initialize form; optimize user permission queryset"""
        super(AbstractUserChangeForm, self).__init__(*args, **kwargs)
        permission_field = self.fields.get('user_permissions', None)
        if permission_field is not None:
            # pre-load content types associated with permissions
            permission_field.queryset = (
                permission_field.queryset.select_related('content_type'))

    def clean_password(self):
        """
        We seek to change the user, but not the password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial['password']


class UserChangeForm(AbstractUserChangeForm):
    """Form to update user, but not their password"""
    class Meta:
        model = User
        fields = '__all__'
