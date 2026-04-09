"""
Auto-numbering service for generating sequential Surat numbers.

Follows SK KPU No. 1257/2024 numbering format:
  External: {NO}/{KLASIFIKASI}-{JENIS}/{SATKER}/{TAHUN}
  Internal: {NO}/{KLASIFIKASI}-{JENIS}/{SATKER}/{SUB_BAGIAN}/{TAHUN}

Uses select_for_update() to ensure thread-safety when
incrementing the counter on NomorSuratCounter.
"""

from django.db import transaction
from django.utils import timezone


@transaction.atomic
def generate_nomor_surat(jenis_naskah, klasifikasi, user, tujuan_surat='external', sub_bagian=None):
    """
    Generate the next sequential letter number.

    Thread-safe: acquires a row-level lock via ``select_for_update`` to
    prevent concurrent duplicate numbers.

    The counter is per unique combination of:
    - External: (jenis_naskah, satker, tahun)
    - Internal: (jenis_naskah, satker, sub_bagian, tahun)
    
    A new counter is auto-created for each new year (yearly reset).

    Args:
        jenis_naskah: JenisNaskahDinas instance.
        klasifikasi: KlasifikasiArsip instance.
        user: User instance (must have ``satker`` set for non-pusat).
        tujuan_surat: 'internal' or 'external' (default: 'external').
        sub_bagian: SubBagian instance (required if tujuan_surat='internal').

    Returns:
        str: Formatted letter number.
            External: ``1/PY.01.1-SD/1101/2024``
            Internal: ``1/PY.01.1-SD/1101/1/2024``
    """
    from apps.master.models import NomorSuratCounter

    now = timezone.localtime()
    current_year = now.year

    # User's SATKER (null = KPU Pusat)
    satker = user.satker if hasattr(user, 'satker') else None

    # For internal letters, sub_bagian is required
    if tujuan_surat == 'internal' and not sub_bagian:
        raise ValueError('Sub Bagian is required for internal letters.')

    # Get or create the counter for this combination
    counter, _created = (
        NomorSuratCounter.objects
        .select_for_update()
        .get_or_create(
            jenis_naskah=jenis_naskah,
            satker=satker,
            sub_bagian=sub_bagian if tujuan_surat == 'internal' else None,
            tahun=current_year,
            defaults={'last_number': 0},
        )
    )

    # Increment
    counter.last_number += 1
    counter.save(update_fields=['last_number'])

    # Build the formatted number
    nomor = str(counter.last_number)
    satker_kode = satker.kode if satker else ''

    # Format: {NO}/{KLASIFIKASI}-{JENIS}/{SATKER}[/{SUB_BAGIAN}]/{TAHUN}
    parts = [nomor]

    klasifikasi_jenis = f"{klasifikasi.kode}-{jenis_naskah.kode}"
    parts.append(klasifikasi_jenis)

    if satker_kode:
        parts.append(satker_kode)

    # Add sub_bagian kode for internal letters
    if tujuan_surat == 'internal' and sub_bagian:
        parts.append(sub_bagian.kode)

    parts.append(str(current_year))

    return '/'.join(parts)
