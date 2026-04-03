"""
Seed script to populate the database with demo data.
Run with: python manage.py shell < seed_data.py
"""

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitapis.settings')
django.setup()

from apps.accounts.models import User
from apps.master.models import UnitKerja, KlasifikasiArsip, JenisNaskahDinas
from apps.surat.models import Surat
from apps.surat.services import generate_nomor_surat
from django.utils import timezone

# Set admin role
admin_user = User.objects.get(username='admin')
admin_user.role = 'admin'
admin_user.first_name = 'Admin'
admin_user.last_name = 'SITAPIS'
admin_user.save()
print("✓ Admin role set")

# Create sample unit kerja (SATKER)
provinsi, _ = UnitKerja.objects.get_or_create(
    kode='18',
    defaults={'nama': 'PROVINSI LAMPUNG'},
)
kabupaten, _ = UnitKerja.objects.get_or_create(
    kode='1801',
    defaults={'nama': 'LAMPUNG SELATAN'},
)
print("✓ Unit Kerja dibuat")

# Create sample klasifikasi arsip
klasifikasi, _ = KlasifikasiArsip.objects.get_or_create(
    kode='PY.01.1',
    defaults={'nama': 'Penyelenggaraan Pemerintahan', 'jenis': 'substantif'},
)
print("✓ Klasifikasi Arsip dibuat")

# Create sample jenis naskah dinas
jenis_surat, _ = JenisNaskahDinas.objects.get_or_create(
    kode='SD',
    defaults={'nama': 'Surat Dinas', 'kategori': 'korespondensi'},
)
print("✓ Jenis Naskah Dinas dibuat")

# Create kasubbag user
kasubbag, created = User.objects.get_or_create(
    username='kasubbag',
    defaults={
        'first_name': 'Kasubbag',
        'last_name': 'Umum',
        'email': 'kasubbag@sitapis.local',
        'role': 'kasubbag',
        'satker': kabupaten,
    },
)
if created:
    kasubbag.set_password('kasubbag123')
    kasubbag.save()
print("✓ User kasubbag dibuat (kasubbag/kasubbag123)")

# Create sekretaris user
sekretaris, created = User.objects.get_or_create(
    username='sekretaris',
    defaults={
        'first_name': 'Sekretaris',
        'last_name': 'Dinas',
        'email': 'sekretaris@sitapis.local',
        'role': 'sekretaris',
        'satker': kabupaten,
    },
)
if created:
    sekretaris.set_password('sekretaris123')
    sekretaris.save()
print("✓ User sekretaris dibuat (sekretaris/sekretaris123)")

# Create staff user
stf, created = User.objects.get_or_create(
    username='staff',
    defaults={
        'first_name': 'Siti',
        'last_name': 'Staff',
        'email': 'staff@sitapis.local',
        'role': 'staff',
        'satker': kabupaten,
    },
)
if created:
    stf.set_password('staff123')
    stf.save()
print("✓ User staff dibuat (staff/staff123)")

# Create sample surat
today = timezone.localdate()
samples = [
    ('Permohonan Pengadaan Peralatan Kantor', today, 'Dinas Pendidikan', 'Bagian Umum'),
    ('Undangan Rapat Koordinasi Q1', today, 'Seluruh Camat', 'Bupati'),
    ('Pemberitahuan Jadwal Pelayanan', today, 'Masyarakat', 'Kepala Dinas'),
]

for perihal, tgl, tujuan, pengirim in samples:
    nomor = generate_nomor_surat(jenis_surat, klasifikasi, stf)
    surat = Surat.objects.create(
        nomor_surat=nomor,
        jenis_naskah=jenis_surat,
        klasifikasi=klasifikasi,
        perihal=perihal,
        tanggal=tgl,
        tujuan=tujuan,
        pengirim=pengirim,
        status=Surat.Status.DRAFT,
        created_by=stf,
    )
    print(f"  → Surat: {nomor}")

print(f"✓ {len(samples)} surat contoh dibuat")
print("\nSelesai! Silakan login ke http://127.0.0.1:8000/")
print("  admin      / admin123      (Administrator)")
print("  sekretaris / sekretaris123 (Sekretaris)")
print("  kasubbag   / kasubbag123   (Kasubbag)")
print("  staff      / staff123      (Staff)")
