"""URL Routing for user account interaction

Uses the HMAC flow from django-registration with the Improved User.

https://django-registration.readthedocs.io/en/latest/hmac.html
https://django-registration.readthedocs.io/en/latest/custom-user.html

Your flake8 config will likely cause imports to be sorted differently.

"""
from django.conf.urls import include, url
from django.contrib.auth import urls as django_auth_urls
from django.views.generic import TemplateView
from registration.backends.hmac.views import ActivationView, RegistrationView

from improved_user.forms import UserCreationForm

urlpatterns = [
    # mimic HMAC-backend URL configuration from django-registration
    url(
        r"^activate/complete/$",
        TemplateView.as_view(
            template_name="registration/activation_complete.html"
        ),
        name="registration_activation_complete",
    ),
    url(
        r"^activate/(?P<activation_key>[-:\w]+)/$",
        ActivationView.as_view(),
        name="registration_activate",
    ),
    url(
        r"^register/$",
        RegistrationView.as_view(form_class=UserCreationForm),
        name="registration_register",
    ),
    url(
        r"^register/complete/$",
        TemplateView.as_view(
            template_name="registration/registration_complete.html"
        ),
        name="registration_complete",
    ),
    url(
        r"^register/closed/$",
        TemplateView.as_view(
            template_name="registration/registration_closed.html"
        ),
        name="registration_disallowed",
    ),
    url(r"^", include(django_auth_urls)),
]
