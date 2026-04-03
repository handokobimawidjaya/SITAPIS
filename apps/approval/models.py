"""
Approval workflow models for tracking document approval history.
"""

from django.conf import settings
from django.db import models


class ApprovalHistory(models.Model):
    """
    Tracks each approval action taken on a Surat.

    Records who performed the action, what action was taken,
    and any comments provided.
    """

    class Action(models.TextChoices):
        """Approval action types."""
        SUBMIT = 'submit', 'Diajukan'
        INPROGRESS = 'inprogress', 'Ditindaklanjuti'
        APPROVE = 'approve', 'Disetujui'
        REJECT = 'reject', 'Ditolak'
        REVISE = 'revise', 'Direvisi'

    surat = models.ForeignKey(
        'surat.Surat',
        on_delete=models.CASCADE,
        related_name='approval_history',
        verbose_name='Surat',
    )
    action = models.CharField(
        max_length=20,
        choices=Action.choices,
        verbose_name='Aksi',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Pengguna',
    )
    comment = models.TextField(blank=True, verbose_name='Komentar')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')

    class Meta:
        verbose_name = 'Riwayat Approval'
        verbose_name_plural = 'Riwayat Approval'
        ordering = ['-timestamp']

    def __str__(self):
        return (
            f"{self.surat.nomor_surat} — "
            f"{self.get_action_display()} oleh {self.user}"
        )
