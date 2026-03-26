"""Approval app configuration."""

from django.apps import AppConfig


class ApprovalConfig(AppConfig):
    """Configuration for the approval workflow app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.approval'
    verbose_name = 'Approval'
