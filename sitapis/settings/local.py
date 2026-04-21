"""
Local development settings — PostgreSQL.
"""

from .base import *  # noqa: F401, F403

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sitapis_db',
        'USER': 'odoo',
        'PASSWORD': 'odoo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
