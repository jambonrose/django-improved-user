"""URL Routing for user account interaction

Uses the HMAC flow from django-registration with the Improved User.

https://django-registration.readthedocs.io/en/latest/hmac.html
https://django-registration.readthedocs.io/en/latest/custom-user.html

Your flake8 config will likely cause imports to be sorted differently.

"""
from django.conf.urls import include, url
from registration.backends.hmac import urls as registration_urls
from registration.backends.hmac.views import RegistrationView

from improved_user.forms import UserCreationForm

urlpatterns = [
    url(r'^register/$',
        RegistrationView.as_view(form_class=UserCreationForm),
        name='registration_register'),
    url(r'^', include(registration_urls)),
]
