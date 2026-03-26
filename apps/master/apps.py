"""Master app configuration."""

from django.apps import AppConfig


class MasterConfig(AppConfig):
    """Configuration for the master data app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.master'
    verbose_name = 'Master Data'
