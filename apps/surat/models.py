"""
Surat (document) models with auto-generated numbering and file attachments.

Surat references JenisNaskahDinas and KlasifikasiArsip directly.
The nomor_surat is auto-generated based on these references plus the
user's SATKER code.
"""

from django.conf import settings
from django.db import models


class Surat(models.Model):
    """
    Main document model representing a letter/surat.

    The nomor_surat is auto-generated when the record is created,
    based on jenis_naskah, klasifikasi, and the user's SATKER.
    Format: {NO}/{KLASIFIKASI}-{JENIS}/{SATKER}/{TAHUN}
    """

    class Status(models.TextChoices):
        """Document lifecycle status."""
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Diajukan'
        APPROVED = 'approved', 'Disetujui'
        REJECTED = 'rejected', 'Ditolak'

    nomor_surat = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nomor Surat',
        help_text='Nomor ter-generate otomatis saat surat dibuat',
    )
    jenis_naskah = models.ForeignKey(
        'master.JenisNaskahDinas',
        on_delete=models.PROTECT,
        verbose_name='Jenis Naskah Dinas',
        null=True,
        blank=True,
    )
    klasifikasi = models.ForeignKey(
        'master.KlasifikasiArsip',
        on_delete=models.PROTECT,
        verbose_name='Klasifikasi Arsip',
        help_text='Kode klasifikasi arsip sesuai substansi surat',
        null=True,
        blank=True,
    )
    perihal = models.CharField(max_length=255, verbose_name='Perihal')
    tanggal = models.DateField(verbose_name='Tanggal Surat')
    tujuan = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Tujuan',
    )
    pengirim = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Pengirim',
    )
    notes = models.TextField(blank=True, verbose_name='Catatan')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Status',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='surat_created',
        verbose_name='Dibuat oleh',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Surat'
        verbose_name_plural = 'Surat'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nomor_surat} — {self.perihal}"

    @property
    def is_editable(self):
        """Check if the document can still be edited."""
        return self.status == self.Status.DRAFT

    @property
    def status_color(self):
        """Return a CSS color class for the current status."""
        colors = {
            self.Status.DRAFT: 'secondary',
            self.Status.SUBMITTED: 'warning',
            self.Status.APPROVED: 'success',
            self.Status.REJECTED: 'danger',
        }
        return colors.get(self.status, 'secondary')


class SuratAttachment(models.Model):
    """File attachment linked to a Surat."""

    surat = models.ForeignKey(
        Surat,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Surat',
    )
    file = models.FileField(
        upload_to='surat_attachments/%Y/%m/',
        verbose_name='File',
    )
    filename = models.CharField(max_length=255, verbose_name='Nama File')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lampiran'
        verbose_name_plural = 'Lampiran'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename
