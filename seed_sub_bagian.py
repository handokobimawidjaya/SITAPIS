"""
Seed script untuk data Sub Bagian.

Menambahkan 4 Sub Bagian default:
1. Keuangan, Umum dan Logistik
2. Teknis Penyelenggaraan Pemilu dan Hukum
3. Perencanaan Data dan Informasi
4. Partisipasi Hubungan Masyarakat dan Sumber Daya Manusia

Run dengan: python3 seed_sub_bagian.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitapis.settings')
django.setup()

from apps.master.models import SubBagian


def seed_sub_bagian():
    """Seed Sub Bagian data."""
    print("=" * 60)
    print("🚀 SEED DATA SUB BAGIAN")
    print("=" * 60)

    sub_bagian_data = [
        {'kode': '1', 'nama': 'Keuangan, Umum dan Logistik'},
        {'kode': '2', 'nama': 'Teknis Penyelenggaraan Pemilu dan Hukum'},
        {'kode': '3', 'nama': 'Perencanaan Data dan Informasi'},
        {'kode': '4', 'nama': 'Partisipasi Hubungan Masyarakat dan Sumber Daya Manusia'},
    ]

    created = 0
    updated = 0

    for data in sub_bagian_data:
        obj, created_flag = SubBagian.objects.update_or_create(
            kode=data['kode'],
            defaults={
                'nama': data['nama'],
                'is_active': True,
            }
        )

        if created_flag:
            created += 1
            print(f"  ✓ Dibuat: {obj.kode} - {obj.nama}")
        else:
            updated += 1
            print(f"  ~ Diperbarui: {obj.kode} - {obj.nama}")

    print("\n" + "=" * 60)
    print(f"📊 TOTAL: {created} dibuat, {updated} diperbarui")
    print("=" * 60)

    # Show all SubBagian
    print("\n📋 Daftar Sub Bagian:")
    for sb in SubBagian.objects.all().order_by('kode'):
        status = "Aktif" if sb.is_active else "Nonaktif"
        print(f"  [{sb.kode}] {sb.nama} - {status}")

    print("\n✓ Seed Sub Bagian selesai!")


if __name__ == '__main__':
    seed_sub_bagian()
