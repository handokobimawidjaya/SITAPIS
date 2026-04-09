"""
Custom User model with role-based access control.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model with role and satker fields."""

    class Role(models.TextChoices):
        """User role choices for access control."""
        ADMIN = 'admin', 'Administrator'
        SEKRETARIS = 'sekretaris', 'Sekretaris'
        KASUBBAG = 'kasubbag', 'Kasubbag'
        STAFF = 'staff', 'Staff'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
        verbose_name='Role',
    )
    satker = models.ForeignKey(
        'master.UnitKerja',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Satuan Kerja',
        help_text='Satuan Kerja tempat user bertugas',
    )
    sub_bagian = models.ForeignKey(
        'master.SubBagian',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Sub Bagian',
        help_text='Sub Bagian tempat user bertugas',
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telepon')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Foto Profil',
    )

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'
        ordering = ['username']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.Role.ADMIN

    @property
    def is_sekretaris(self):
        """Check if user has sekretaris role."""
        return self.role == self.Role.SEKRETARIS

    @property
    def is_kasubbag(self):
        """Check if user has kasubbag role."""
        return self.role == self.Role.KASUBBAG

    @property
    def is_staff_role(self):
        """Check if user has staff role."""
        return self.role == self.Role.STAFF
