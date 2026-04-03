"""
Views for the master data app: full CRUD for all master models.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import role_required

from .forms import (
    JenisNaskahDinasForm,
    KlasifikasiArsipForm,
    UnitKerjaForm,
)
from .models import (
    JenisNaskahDinas,
    KlasifikasiArsip,
    UnitKerja,
)


# ── Helper for generic CRUD ────────────────────────────────────────────

def _generic_list(request, model_class, template, query_field='nama'):
    """Generic list view with search."""
    items = model_class.objects.all()
    query = request.GET.get('q', '')
    if query:
        items = items.filter(**{f'{query_field}__icontains': query})
    return render(request, template, {'items': items, 'query': query})


def _generic_create(request, form_class, template, list_url, title, success_msg):
    """Generic create view."""
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_msg)
        return redirect(list_url)
    return render(request, template, {'form': form, 'title': title})


def _generic_update(request, model_class, form_class, template, list_url, pk, title_prefix, success_msg):
    """Generic update view."""
    obj = get_object_or_404(model_class, pk=pk)
    form = form_class(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_msg)
        return redirect(list_url)
    return render(request, template, {'form': form, 'title': f'{title_prefix}: {obj}'})


def _generic_delete(request, model_class, pk, list_url, success_msg):
    """Generic delete view."""
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, success_msg)
        return redirect(list_url)
    return render(request, 'master/confirm_delete.html', {
        'object': obj,
        'back_url': list_url,
    })


# ── Klasifikasi Arsip ──────────────────────────────────────────────────

@login_required
@role_required('admin', 'sekretaris')
def klasifikasi_arsip_list(request):
    """List all archive classification codes."""
    return _generic_list(
        request, KlasifikasiArsip,
        'master/klasifikasi_arsip_list.html',
    )


@login_required
@role_required('admin')
def klasifikasi_arsip_create(request):
    """Create a new archive classification code."""
    return _generic_create(
        request, KlasifikasiArsipForm,
        'master/klasifikasi_arsip_form.html',
        'master:klasifikasi_arsip_list',
        'Tambah Klasifikasi Arsip',
        'Klasifikasi Arsip berhasil dibuat.',
    )


@login_required
@role_required('admin')
def klasifikasi_arsip_update(request, pk):
    """Update an existing archive classification code."""
    return _generic_update(
        request, KlasifikasiArsip, KlasifikasiArsipForm,
        'master/klasifikasi_arsip_form.html',
        'master:klasifikasi_arsip_list', pk,
        'Edit Klasifikasi Arsip',
        'Klasifikasi Arsip berhasil diperbarui.',
    )


@login_required
@role_required('admin')
def klasifikasi_arsip_delete(request, pk):
    """Delete an archive classification code."""
    return _generic_delete(
        request, KlasifikasiArsip, pk,
        'master:klasifikasi_arsip_list',
        'Klasifikasi Arsip berhasil dihapus.',
    )


# ── Jenis Naskah Dinas ─────────────────────────────────────────────────

@login_required
@role_required('admin', 'sekretaris')
def jenis_naskah_list(request):
    """List all letter types."""
    return _generic_list(
        request, JenisNaskahDinas,
        'master/jenis_naskah_list.html',
    )


@login_required
@role_required('admin')
def jenis_naskah_create(request):
    """Create a new letter type."""
    return _generic_create(
        request, JenisNaskahDinasForm,
        'master/jenis_naskah_form.html',
        'master:jenis_naskah_list',
        'Tambah Jenis Naskah Dinas',
        'Jenis Naskah Dinas berhasil dibuat.',
    )


@login_required
@role_required('admin')
def jenis_naskah_update(request, pk):
    """Update an existing letter type."""
    return _generic_update(
        request, JenisNaskahDinas, JenisNaskahDinasForm,
        'master/jenis_naskah_form.html',
        'master:jenis_naskah_list', pk,
        'Edit Jenis Naskah Dinas',
        'Jenis Naskah Dinas berhasil diperbarui.',
    )


@login_required
@role_required('admin')
def jenis_naskah_delete(request, pk):
    """Delete a letter type."""
    return _generic_delete(
        request, JenisNaskahDinas, pk,
        'master:jenis_naskah_list',
        'Jenis Naskah Dinas berhasil dihapus.',
    )


# ── Unit Kerja ──────────────────────────────────────────────────────────

@login_required
@role_required('admin', 'sekretaris')
def unit_kerja_list(request):
    """List all organizational units."""
    return _generic_list(
        request, UnitKerja,
        'master/unit_kerja_list.html',
    )


@login_required
@role_required('admin')
def unit_kerja_create(request):
    """Create a new organizational unit."""
    return _generic_create(
        request, UnitKerjaForm,
        'master/unit_kerja_form.html',
        'master:unit_kerja_list',
        'Tambah Unit Kerja',
        'Unit Kerja berhasil dibuat.',
    )


@login_required
@role_required('admin')
def unit_kerja_update(request, pk):
    """Update an existing organizational unit."""
    return _generic_update(
        request, UnitKerja, UnitKerjaForm,
        'master/unit_kerja_form.html',
        'master:unit_kerja_list', pk,
        'Edit Unit Kerja',
        'Unit Kerja berhasil diperbarui.',
    )


@login_required
@role_required('admin')
def unit_kerja_delete(request, pk):
    """Delete an organizational unit."""
    return _generic_delete(
        request, UnitKerja, pk,
        'master:unit_kerja_list',
        'Unit Kerja berhasil dihapus.',
    )
