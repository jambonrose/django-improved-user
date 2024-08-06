"""Forms for Creating and Updating Improved Users"""

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

User = get_user_model()  # pylint: disable=invalid-name


class AbstractUserCreationForm(forms.ModelForm):
    """Abstract Form to create an unprivileged user

    Create a User with no permissions based on username and password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
        strip=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
        strip=False,
    )

    def clean_password2(self):
        """Check wether password 1 and password 2 are equivalent

        While ideally this would be done in clean, there is a chance a
        superclass could declare clean and forget to call super. We
        therefore opt to run this password mismatch check in password2
        clean, but to show the error above password1 (as we are unsure
        whether password 1 or password 2 contains the typo, and putting
        it above password 2 may lead some users to believe the typo is
        in just one).

        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error(
                "password1",
                forms.ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                ),
            )
        return password2

    def _post_clean(self):
        """Run password validaton after clean methods

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
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", error)

    def save(self, commit=True):
        """Save the user; use password hasher to set password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(AbstractUserCreationForm):
    """Form to create an unprivileged user

    A concrete implementation of AbstractUserCreationForm that uses an
    e-mail address as a user's identifier.
    """

    error_messages = {
        **AbstractUserCreationForm.error_messages,
        "duplicate_email": _("A user with that email already exists."),
    }

    class Meta:
        model = User
        fields = ("email", "full_name", "short_name")

    def clean_email(self):
        """Clean email; set nice error message

        Since User.email is unique, this check is redundant,
        but it sets a nicer error message than the ORM. See #13147.

        https://code.djangoproject.com/ticket/13147
        """
        email = self.cleaned_data["email"]
        try:
            # https://docs.djangoproject.com/en/stable/topics/db/managers/#default-managers
            # pylint: disable=protected-access
            User._default_manager.get(email=email)
            # pylint: enable=protected-access
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"],
            code="duplicate_email",
        )


class AbstractUserChangeForm(forms.ModelForm):
    """Base form update User, but not their password"""

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    rel_password_url = None

    def __init__(self, *args, **kwargs):
        """Initialize form; optimize user permission queryset"""
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = self.fields[
            "password"
        ].help_text.format(self.get_local_password_path())
        permission_field = self.fields.get("user_permissions", None)
        if permission_field is not None:
            # pre-load content types associated with permissions
            permission_field.queryset = (
                permission_field.queryset.select_related("content_type")
            )

    def get_local_password_path(self):
        """Return relative path to password form

        Will return rel_password_url attribute on form
        or else '../password/'. If subclasses cannot simply replace
        rel_password_url, then they can override this method instead of
        __init__.

        """
        if (
            hasattr(self, "rel_password_url")
            and self.rel_password_url is not None
        ):
            return self.rel_password_url
        return "../password/"

    def clean_password(self):
        """Change user info; not the password

        We seek to change the user, but not the password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]


class UserChangeForm(AbstractUserChangeForm):
    """Form to update user, but not their password"""

    class Meta:
        model = User
        fields = "__all__"
