from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import User

try:
    from django.contrib.auth import password_validation
except ImportError:
    # Django 1.8 doesn't have password strength validation
    # Insert a dummy object into the namespace.
    class EmptyValidator:
        def validate_password(self, password, instance):
            pass

        def password_validators_help_text_html(self):
            return None

    password_validation = EmptyValidator()


class AbstractUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given
    username and password.
    """
    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()  # creates self.instance
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", error)

    def save(self, commit=True):
        user = super(AbstractUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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
    #     "duplicate_email": _("A user with that email already exists."),
    # }
    error_messages = {
        k: v
        for d in [
            AbstractUserCreationForm.error_messages,
            { "duplicate_email": _("A user with that email already exists.")}]
        for k, v in d.items()
    }

    class Meta:
        model = User
        fields = ("email", "full_name", "short_name")

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"],
            code="duplicate_email",
        )


class AbstractUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def __init__(self, *args, **kwargs):
        super(AbstractUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get("user_permissions", None)
        if f is not None:
            f.queryset = f.queryset.select_related("content_type")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserChangeForm(AbstractUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
