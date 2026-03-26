"""
Master data models for KPU official letter management.

Based on SK KPU No. 1257 Tahun 2024 tentang Kode Klasifikasi Arsip
dan Pengkodean Naskah Dinas.
"""

from django.db import models


class KlasifikasiArsip(models.Model):
    """
    Hierarchical archive classification code.

    Supports multi-level codes like PP → PP.01 → PP.01.1.
    Divided into two types: Substantif (core functions) and
    Fasilitatif (supporting functions).
    """

    class Jenis(models.TextChoices):
        """Archive classification type."""
        SUBSTANTIF = 'substantif', 'Substantif'
        FASILITATIF = 'fasilitatif', 'Fasilitatif'

    kode = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Kode',
        help_text='Contoh: PP, PP.01, PP.01.1',
    )
    nama = models.CharField(max_length=255, verbose_name='Nama')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi')
    jenis = models.CharField(
        max_length=15,
        choices=Jenis.choices,
        verbose_name='Jenis Klasifikasi',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent',
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Klasifikasi Arsip'
        verbose_name_plural = 'Klasifikasi Arsip'
        ordering = ['kode']

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    @property
    def full_path(self):
        """Return the full hierarchical path, e.g. 'PP > PP.01 > PP.01.1'."""
        parts = [self.kode]
        node = self.parent
        while node:
            parts.insert(0, node.kode)
            node = node.parent
        return ' > '.join(parts)


class JenisNaskahDinas(models.Model):
    """
    Official letter type code.

    Maps letter types to their abbreviation codes as defined
    in Lampiran II SK KPU No. 1257/2024.
    """

    kode = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Kode',
        help_text='Contoh: SD, ND, ST',
    )
    nama = models.CharField(max_length=100, verbose_name='Nama')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Jenis Naskah Dinas'
        verbose_name_plural = 'Jenis Naskah Dinas'
        ordering = ['kode']

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class UnitKerja(models.Model):
    """
    Organizational unit hierarchy: Biro → Bagian → Subbagian.

    Codes are used in the letter numbering system to identify
    the originating bureau/division.
    """

    kode = models.CharField(
        max_length=10,
        verbose_name='Kode',
        help_text='Contoh: 01, 1, 1.1',
    )
    nama = models.CharField(max_length=255, verbose_name='Nama')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unit Kerja'
        verbose_name_plural = 'Unit Kerja'
        ordering = ['kode']

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Wilayah(models.Model):
    """
    Region hierarchy: Provinsi → Kabupaten/Kota.

    Used in letter numbering for KPU Provinsi and Kabupaten/Kota
    level documents. Also used as SATKER (Satuan Kerja) for users.
    """

    class Level(models.TextChoices):
        """Region hierarchy level."""
        PROVINSI = 'provinsi', 'Provinsi'
        KABUPATEN_KOTA = 'kabupaten_kota', 'Kabupaten/Kota'

    kode = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Kode',
        help_text='Contoh: 11 (Aceh), 1101 (Kab. Aceh Selatan)',
    )
    nama = models.CharField(max_length=255, verbose_name='Nama')
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        verbose_name='Level',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Provinsi',
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wilayah'
        verbose_name_plural = 'Wilayah'
        ordering = ['kode']

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class NomorSuratCounter(models.Model):
    """
    Sequential counter for letter numbering.

    Tracks the last-used number per unique combination of
    (jenis_naskah, satker, tahun). Resets automatically each year
    when a new year's first letter is generated.
    """

    jenis_naskah = models.ForeignKey(
        JenisNaskahDinas,
        on_delete=models.PROTECT,
        verbose_name='Jenis Naskah Dinas',
    )
    satker = models.ForeignKey(
        UnitKerja,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Satuan Kerja',
        help_text='Null = KPU Pusat',
    )
    tahun = models.PositiveIntegerField(verbose_name='Tahun')
    last_number = models.PositiveIntegerField(
        default=0,
        verbose_name='Nomor Terakhir',
    )

    class Meta:
        verbose_name = 'Counter Nomor Surat'
        verbose_name_plural = 'Counter Nomor Surat'
        unique_together = [['jenis_naskah', 'satker', 'tahun']]
        ordering = ['-tahun', 'jenis_naskah']

    def __str__(self):
        satker_name = self.satker.nama if self.satker_id else 'KPU Pusat'
        return (
            f"{self.jenis_naskah.kode} - {satker_name} "
            f"({self.tahun}) #{self.last_number}"
        )
