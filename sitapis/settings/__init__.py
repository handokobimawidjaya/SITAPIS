"""
Settings package.
Default to local settings for development.
Use DJANGO_SETTINGS_MODULE=sitapis.settings.production for production.
"""
from .local import *  # noqa: F401, F403
