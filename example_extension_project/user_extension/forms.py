"""Forms for User extension example project"""
from improved_user.forms import (
    AbstractUserChangeForm, UserCreationForm as AbstractUserCreationForm,
)

from .models import User


class UserCreationForm(AbstractUserCreationForm):
    """A subclass of Improved User's UserCreationForm"""

    class Meta(AbstractUserCreationForm.Meta):
        model = User


class UserChangeForm(AbstractUserChangeForm):
    """Form to update user, but not their password"""
    class Meta:
        model = User
        fields = '__all__'
