"""
Views for the surat (document) app: CRUD, dashboard, and file attachments.
"""

import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import role_required

from .forms import SuratAttachmentForm, SuratForm, SuratMasukForm, SuratMasukTindakLanjutForm
from .models import Surat, SuratAttachment, SuratMasuk
from .services import generate_nomor_surat


@login_required
def dashboard(request):
    """Main dashboard with statistics and recent documents."""
    total_keluar = Surat.objects.count()
    total_masuk = SuratMasuk.objects.count()
    draft = Surat.objects.filter(status=Surat.Status.DRAFT).count()
    submitted = Surat.objects.filter(status=Surat.Status.SUBMITTED).count()
    approved = Surat.objects.filter(status=Surat.Status.APPROVED).count()
    rejected = Surat.objects.filter(status=Surat.Status.REJECTED).count()
    recent = Surat.objects.select_related(
        'jenis_naskah', 'klasifikasi', 'created_by',
    ).order_by('-created_at')[:10]

    # Monthly chart data (last 12 months)
    from django.db.models.functions import TruncMonth
    monthly_data = (
        Surat.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )[:12]

    chart_labels = [
        item['month'].strftime('%b %Y') for item in monthly_data
    ] if monthly_data else []
    chart_values = [
        item['count'] for item in monthly_data
    ] if monthly_data else []

    return render(request, 'dashboard.html', {
        'total_keluar': total_keluar,
        'total_masuk': total_masuk,
        'draft': draft,
        'submitted': submitted,
        'approved': approved,
        'rejected': rejected,
        'recent': recent,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    })


@login_required
def surat_list(request):
    """List all documents with search, filter, and pagination."""
    queryset = Surat.objects.select_related(
        'jenis_naskah', 'klasifikasi', 'created_by',
    ).all()

    # Search
    query = request.GET.get('q', '')
    if query:
        queryset = queryset.filter(
            Q(nomor_surat__icontains=query)
            | Q(perihal__icontains=query)
            | Q(tujuan__icontains=query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    paginator = Paginator(queryset, 15)
    page = request.GET.get('page')
    surat_page = paginator.get_page(page)

    return render(request, 'surat/surat_list.html', {
        'page_obj': surat_page,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Surat.Status.choices,
    })


@login_required
def surat_create(request):
    """Create a new document with auto-generated number."""
    # Set default pengirim to user's satker name with KPU prefix
    initial = {}
    if request.user.satker:
        initial['pengirim'] = 'KPU ' + request.user.satker.nama

    form = SuratForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        surat = form.save(commit=False)
        surat.created_by = request.user
        surat.nomor_surat = generate_nomor_surat(
            surat.jenis_naskah, surat.klasifikasi, request.user,
        )
        surat.save()

        messages.success(
            request,
            f'Surat berhasil dibuat dengan nomor: {surat.nomor_surat}',
        )
        return redirect('surat:surat_detail', pk=surat.pk)

    return render(request, 'surat/surat_form.html', {
        'form': form,
        'title': 'Buat Surat Baru',
    })


@login_required
def surat_detail(request, pk):
    """View document details with approval history."""
    surat = get_object_or_404(
        Surat.objects.select_related('jenis_naskah', 'klasifikasi', 'created_by'),
        pk=pk,
    )
    attachments = surat.attachments.all()
    history = surat.approval_history.select_related('user').all()

    return render(request, 'surat/surat_detail.html', {
        'surat': surat,
        'attachments': attachments,
        'history': history,
    })


@login_required
def surat_update(request, pk):
    """Update a document (only if still in draft or inprogress for attachment)."""
    surat = get_object_or_404(Surat, pk=pk)
    
    # Allow edit only if draft or inprogress
    if surat.status not in [Surat.Status.DRAFT, Surat.Status.INPROGRESS]:
        messages.error(request, 'Surat tidak dapat diedit karena status sudah '+ surat.get_status_display() +'.')
        return redirect('surat:surat_detail', pk=pk)

    form = SuratForm(request.POST or None, instance=surat)
    if request.method == 'POST' and form.is_valid():
        form.save()
        
        # Handle attachment upload when status is INPROGRESS
        if surat.status == Surat.Status.INPROGRESS:
            files = request.FILES.getlist('attachments')
            if files:
                for f in files:
                    SuratAttachment.objects.create(
                        surat=surat,
                        file=f,
                        filename=f.name,
                    )
                messages.success(request, 'Surat berhasil diperbarui dan lampiran diupload.')
                return redirect('surat:surat_detail', pk=surat.pk)
            else:
                messages.info(request, 'Surat berhasil diperbarui. Upload lampiran untuk menyelesaikan surat.')
        else:
            messages.success(request, 'Surat berhasil diperbarui.')
        
        return redirect('surat:surat_detail', pk=surat.pk)

    attachments = surat.attachments.all() if surat.pk else []
    return render(request, 'surat/surat_form.html', {
        'form': form,
        'title': f'Edit Surat: {surat.nomor_surat}',
        'surat': surat,
        'attachments': attachments,
    })


@login_required
def surat_delete(request, pk):
    """Delete a document (only if still in draft)."""
    surat = get_object_or_404(Surat, pk=pk)
    if not surat.is_editable:
        messages.error(request, 'Surat tidak dapat dihapus karena sudah diajukan.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        surat.delete()
        messages.success(request, 'Surat berhasil dihapus.')
        return redirect('surat:surat_list')

    return render(request, 'surat/confirm_delete.html', {
        'object': surat,
        'back_url': 'surat:surat_list',
    })


@login_required
def attachment_delete(request, pk):
    """Delete a single attachment."""
    attachment = get_object_or_404(SuratAttachment, pk=pk)
    surat_pk = attachment.surat.pk

    if not attachment.surat.is_editable:
        messages.error(request, 'Lampiran tidak dapat dihapus.')
        return redirect('surat:surat_detail', pk=surat_pk)

    if request.method == 'POST':
        # Delete the file from storage
        if attachment.file and os.path.isfile(attachment.file.path):
            os.remove(attachment.file.path)
        attachment.delete()
        messages.success(request, 'Lampiran berhasil dihapus.')

    return redirect('surat:surat_update', pk=surat_pk)

# ==============================================================================
# SURAT MASUK VIEWS
# ==============================================================================

@login_required
def surat_masuk_list(request):
    """List all incoming documents with search and filter."""
    queryset = SuratMasuk.objects.select_related('disposisi', 'created_by').all()

    query = request.GET.get('q', '')
    if query:
        queryset = queryset.filter(
            Q(nomor_surat__icontains=query)
            | Q(perihal__icontains=query)
            | Q(pengirim__icontains=query)
        )

    status_filter = request.GET.get('status', '')
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    paginator = Paginator(queryset, 15)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'surat/surat_masuk_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'status_choices': SuratMasuk.Status.choices,
    })


@login_required
def surat_masuk_create(request):
    """Create a new incoming document."""
    form = SuratMasukForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        action = request.POST.get('action', 'draft') # 'draft' or 'disposisi'
        
        if form.is_valid():
            surat_masuk = form.save(commit=False)
            surat_masuk.created_by = request.user
            
            # Validation for disposisi
            if action == 'disposisi':
                if not surat_masuk.lampiran_surat:
                    messages.error(request, 'Lampiran surat (Scan PDF) wajib di-upload untuk melakukan disposisi.')
                    return render(request, 'surat/surat_masuk_form.html', {'form': form, 'title': 'Buat Surat Masuk'})
                surat_masuk.status = SuratMasuk.Status.INPROGRESS
            else:
                surat_masuk.status = SuratMasuk.Status.DRAFT

            surat_masuk.save()
            messages.success(request, f'Surat Masuk berhasil disimpan sebagai {surat_masuk.get_status_display()}.')
            return redirect('surat:surat_masuk_detail', pk=surat_masuk.pk)

    return render(request, 'surat/surat_masuk_form.html', {
        'form': form,
        'title': 'Buat Surat Masuk',
    })


@login_required
def surat_masuk_detail(request, pk):
    """View incoming document details and handle Tindak Lanjut."""
    surat_masuk = get_object_or_404(
        SuratMasuk.objects.select_related('disposisi', 'created_by'),
        pk=pk,
    )

    tindak_lanjut_form = None
    if surat_masuk.status == SuratMasuk.Status.INPROGRESS and request.user == surat_masuk.disposisi:
        tindak_lanjut_form = SuratMasukTindakLanjutForm(request.POST or None, instance=surat_masuk)
        
        if request.method == 'POST' and tindak_lanjut_form.is_valid():
            surat = tindak_lanjut_form.save(commit=False)
            surat.status = SuratMasuk.Status.DONE
            surat.save()
            messages.success(request, 'Surat Masuk berhasil ditindaklanjuti dan diselesaikan.')
            return redirect('surat:surat_masuk_detail', pk=surat.pk)

    return render(request, 'surat/surat_masuk_detail.html', {
        'surat_masuk': surat_masuk,
        'tindak_lanjut_form': tindak_lanjut_form,
    })


@login_required
def surat_masuk_update(request, pk):
    """Update incoming document."""
    surat_masuk = get_object_or_404(SuratMasuk, pk=pk)
    
    if surat_masuk.status == SuratMasuk.Status.DONE:
        messages.error(request, 'Surat yang sudah selesai tidak dapat diedit.')
        return redirect('surat:surat_masuk_detail', pk=pk)

    form = SuratMasukForm(request.POST or None, request.FILES or None, instance=surat_masuk)
    
    if request.method == 'POST':
        action = request.POST.get('action', 'draft') # 'draft' or 'disposisi'
        
        if form.is_valid():
            sm = form.save(commit=False)
            
            if action == 'disposisi':
                if not sm.lampiran_surat:
                    messages.error(request, 'Lampiran surat (Scan PDF) wajib di-upload untuk melakukan disposisi.')
                    return render(request, 'surat/surat_masuk_form.html', {'form': form, 'title': f'Edit Surat Masuk: {surat_masuk.nomor_surat}', 'surat_masuk': surat_masuk})
                sm.status = SuratMasuk.Status.INPROGRESS
            # If draft, maintain draft status if currently draft, else maintain inprogress
            
            sm.save()
            messages.success(request, 'Surat Masuk berhasil diperbarui.')
            return redirect('surat:surat_masuk_detail', pk=sm.pk)

    return render(request, 'surat/surat_masuk_form.html', {
        'form': form,
        'title': f'Edit Surat Masuk: {surat_masuk.nomor_surat}',
        'surat_masuk': surat_masuk,
    })


@login_required
def surat_masuk_delete(request, pk):
    """Delete incoming document."""
    surat_masuk = get_object_or_404(SuratMasuk, pk=pk)
    if surat_masuk.status != SuratMasuk.Status.DRAFT:
        messages.error(request, 'Hanya Surat Masuk berstatus Draft yang dapat dihapus.')
        return redirect('surat:surat_masuk_detail', pk=pk)

    if request.method == 'POST':
        surat_masuk.lampiran_surat.delete(save=False)
        surat_masuk.delete()
        messages.success(request, 'Surat Masuk berhasil dihapus.')
        return redirect('surat:surat_masuk_list')

    return render(request, 'surat/confirm_delete.html', {
        'object': surat_masuk,
        'back_url': 'surat:surat_masuk_list',
        'is_surat_masuk': True,
    })
