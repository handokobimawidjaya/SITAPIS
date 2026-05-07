import logging
from django.core.management.base import BaseCommand
from apps.surat.models import Surat
from apps.master.models import NomorSuratCounter

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync NomorSuratCounter based on existing data in Surat (Useful after manual SQL inserts)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Mulai menyinkronkan nomor surat...")
        
        updated_count = 0
        for surat in Surat.objects.all():
            if not surat.nomor_surat:
                continue
                
            try:
                # Ambil angka paling depan sebelum '/'
                # Contoh: '21/PK.01-BA/1807/2026' -> '21'
                base_str = str(surat.nomor_surat).split('/')[0]
                # Tangani huruf di belakang nomor (misal '59.a')
                base_str = base_str.split('.')[0]
                number = int(base_str)
            except Exception:
                continue

            # Tentukan satker (mengikuti logika generate_nomor_surat)
            satker = None
            if surat.created_by and hasattr(surat.created_by, 'satker'):
                satker = surat.created_by.satker

            if not surat.jenis_naskah:
                continue

            counter, created = NomorSuratCounter.objects.get_or_create(
                jenis_naskah=surat.jenis_naskah,
                satker=satker,
                sub_bagian=None,
                tahun=surat.tanggal.year,
                defaults={'last_number': number}
            )

            if not created and number > counter.last_number:
                counter.last_number = number
                counter.save(update_fields=['last_number'])
                updated_count += 1
                self.stdout.write(f"Diperbarui: {surat.jenis_naskah.kode} tahun {surat.tanggal.year} menjadi nomor terakhir {number}")

        self.stdout.write(self.style.SUCCESS(f"Selesai! {updated_count} counter berhasil disinkronkan ke angka tertinggi."))
