"""Surat app configuration."""

from django.apps import AppConfig


class SuratConfig(AppConfig):
    """Configuration for the surat (document) app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.surat'
    verbose_name = 'Surat'
