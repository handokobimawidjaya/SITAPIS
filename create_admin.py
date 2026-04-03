# -*- coding: utf-8 -*-
"""
Script untuk membuat user admin.
Run: python create_admin.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitapis.settings')
django.setup()

from apps.accounts.models import User

# Create admin user
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'first_name': 'Admin',
        'last_name': 'SITAPIS',
        'email': 'admin@sitapis.local',
        'role': 'admin',
    }
)

if created:
    admin.set_password('admin123')
    admin.save()
    print("User admin berhasil dibuat!")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Role: Administrator")
else:
    print("User admin sudah ada.")
    print("  Username: %s" % admin.username)
    print("  Role: %s" % admin.role)
