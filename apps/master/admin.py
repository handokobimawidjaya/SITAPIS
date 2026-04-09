"""
Django admin registration for all master data models.
"""

from django.contrib import admin

from .models import (
    JenisNaskahDinas,
    KlasifikasiArsip,
    SubBagian,
    UnitKerja,
)


@admin.register(KlasifikasiArsip)
class KlasifikasiArsipAdmin(admin.ModelAdmin):
    """Admin for archive classification codes."""

    list_display = ['kode', 'nama', 'jenis', 'parent', 'is_active']
    list_filter = ['jenis', 'is_active']
    search_fields = ['kode', 'nama']
    list_editable = ['is_active']
    raw_id_fields = ['parent']


@admin.register(JenisNaskahDinas)
class JenisNaskahDinasAdmin(admin.ModelAdmin):
    """Admin for letter type codes."""

    list_display = ['kode', 'nama', 'is_active']
    list_filter = ['is_active']
    search_fields = ['kode', 'nama']
    list_editable = ['is_active']


@admin.register(UnitKerja)
class UnitKerjaAdmin(admin.ModelAdmin):
    """Admin for organizational unit hierarchy."""

    list_display = ['kode', 'nama', 'is_active']
    search_fields = ['kode', 'nama']
    list_editable = ['is_active']


@admin.register(SubBagian)
class SubBagianAdmin(admin.ModelAdmin):
    """Admin for Sub Bagian."""

    list_display = ['kode', 'nama', 'is_active']
    search_fields = ['kode', 'nama']
    list_editable = ['is_active']
