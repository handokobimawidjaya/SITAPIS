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


@transaction.atomic
def generate_backdate_nomor_surat(surat, user):
    """
    Generate letter number specifically for backdate documents.
    Logic Priority:
    1. Re-use lowest Cancelled/Rejected number on the same date.
    2. Add alphabetical suffix (e.g. .a, .b) to the max number on that date.
    3. If no letter on that exact date, find max number before that date.
    """
    from apps.surat.models import Surat

    satker = user.satker if hasattr(user, 'satker') else None
    satker_kode = satker.kode if satker else ''

    # Build the suffix format mapping
    parts_tail = [f"{surat.klasifikasi.kode}-{surat.jenis_naskah.kode}"]
    if satker_kode:
        parts_tail.append(satker_kode)
    if surat.tujuan_surat == 'internal' and surat.sub_bagian:
        parts_tail.append(surat.sub_bagian.kode)
    parts_tail.append(str(surat.tanggal.year))

    tail_str = '/' + '/'.join(parts_tail)

    base_qs = Surat.objects.filter(
        tanggal=surat.tanggal,
        jenis_naskah=surat.jenis_naskah,
        klasifikasi=surat.klasifikasi,
        sub_bagian=surat.sub_bagian,
        tujuan_surat=surat.tujuan_surat,
    )
    if surat.pk:
        base_qs = base_qs.exclude(pk=surat.pk)

    def get_prefix(nomor):
        try:
            return nomor.split('/')[0]
        except:
            return '0'

    def prefix_sort_key(p):
        parts = p.split('.')
        try:
            num = int(parts[0])
        except ValueError:
            num = 0
        return (num, parts[1] if len(parts) > 1 else '')

    # Prioritas 1: Cari yang tercancel di hari yang sama
    rejected_surat = base_qs.filter(status=Surat.Status.REJECTED)
    rejected_prefixes = [get_prefix(rs.nomor_surat) for rs in rejected_surat]

    if rejected_prefixes:
        rejected_prefixes.sort(key=prefix_sort_key)
        return f"{rejected_prefixes[0]}{tail_str}"

    # Prioritas 2: Angka maksimal + suffix di hari yang sama
    all_prefixes = [get_prefix(s.nomor_surat) for s in base_qs]

    if not all_prefixes:
        # Jika gak ada surat di hari tsb, cari yg sebelum tanggal tsb
        previous_qs = Surat.objects.filter(
            tanggal__lt=surat.tanggal,
            tanggal__year=surat.tanggal.year,
            jenis_naskah=surat.jenis_naskah,
            klasifikasi=surat.klasifikasi,
            sub_bagian=surat.sub_bagian,
            tujuan_surat=surat.tujuan_surat,
        )
        if surat.pk:
            previous_qs = previous_qs.exclude(pk=surat.pk)
        
        all_prefixes = [get_prefix(s.nomor_surat) for s in previous_qs]

    if not all_prefixes:
        return f"1{tail_str}"

    all_prefixes.sort(key=prefix_sort_key)
    max_prefix = all_prefixes[-1]

    parts = max_prefix.split('.')
    try:
        base_num = int(parts[0])
    except ValueError:
        base_num = 0

    # Collect existing suffixes for that exact base_num in the entire year to be safe against collisions
    year_qs = Surat.objects.filter(
        tanggal__year=surat.tanggal.year,
        jenis_naskah=surat.jenis_naskah,
        klasifikasi=surat.klasifikasi,
        sub_bagian=surat.sub_bagian,
        tujuan_surat=surat.tujuan_surat,
    )
    if surat.pk:
        year_qs = year_qs.exclude(pk=surat.pk)
    
    year_prefixes = [get_prefix(s.nomor_surat) for s in year_qs]
    existing_suffixes = [p.split('.')[1] for p in year_prefixes if p.startswith(str(base_num)+'.') and len(p.split('.')) > 1]

    import string
    for char in string.ascii_lowercase:
        if char not in existing_suffixes:
            return f"{base_num}.{char}{tail_str}"

    return f"{base_num}.z{tail_str}"
