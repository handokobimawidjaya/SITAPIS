"""
Django admin configuration for accounts, surat, and approval apps.
"""

from django.contrib import admin

from apps.accounts.models import User
from apps.surat.models import Surat, SuratAttachment
from apps.approval.models import ApprovalHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin view for User model."""
    list_display = ['username', 'get_full_name', 'email', 'role', 'satker', 'is_active']
    list_filter = ['role', 'is_active', 'satker']
    search_fields = ['username', 'first_name', 'last_name', 'email']


class SuratAttachmentInline(admin.TabularInline):
    """Inline attachments in Surat admin."""
    model = SuratAttachment
    extra = 0


@admin.register(Surat)
class SuratAdmin(admin.ModelAdmin):
    """Admin view for Surat model."""
    list_display = ['nomor_surat', 'perihal', 'tanggal', 'status', 'created_by']
    list_filter = ['status', 'jenis_naskah', 'klasifikasi']
    search_fields = ['nomor_surat', 'perihal']
    inlines = [SuratAttachmentInline]


@admin.register(ApprovalHistory)
class ApprovalHistoryAdmin(admin.ModelAdmin):
    """Admin view for ApprovalHistory model."""
    list_display = ['surat', 'action', 'user', 'timestamp']
    list_filter = ['action']
