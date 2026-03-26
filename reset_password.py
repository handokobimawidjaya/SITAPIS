"""
Script untuk reset password user.

Usage: python3 reset_password.py <username> <new_password>

Contoh: python3 reset_password.py admin admin123
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simonas.settings')
django.setup()

from apps.accounts.models import User


def reset_password(username, new_password):
    """Reset password untuk user tertentu."""
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"✓ Password untuk '{username}' berhasil direset!")
        print(f"  Username: {username}")
        print(f"  Password: {new_password}")
        print(f"  Name: {user.get_full_name()}")
        print(f"  Role: {user.role}")
    except User.DoesNotExist:
        print(f"✗ User '{username}' tidak ditemukan!")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 reset_password.py <username> <new_password>")
        print()
        print("Contoh:")
        print("  python3 reset_password.py admin admin123")
        print()
        print("Atau jalankan tanpa argumen untuk reset user admin dengan password default:")
        print("  python3 reset_password.py")
        print()
        
        # Default: reset admin password
        print("Reset password admin dengan default (admin123)?")
        response = input("Ketik 'y' untuk ya, atau username untuk user lain: ").strip()
        
        if response.lower() == 'y':
            reset_password('admin', 'admin123')
        elif response.strip():
            username = response.strip()
            password = input(f"Password baru untuk {username}: ").strip()
            if password:
                reset_password(username, password)
            else:
                print("✗ Password tidak boleh kosong!")
                sys.exit(1)
        else:
            print("✗ Tidak ada input!")
            sys.exit(1)
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        reset_password(username, password)
