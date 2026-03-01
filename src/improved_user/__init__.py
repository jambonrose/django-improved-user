"""Compose new Django User models that follow best-practices for international names and authenticate via email instead of username."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-improved-user")
except PackageNotFoundError:
    __version__ = "0.0.0"
