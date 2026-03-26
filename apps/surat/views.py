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

from .forms import SuratAttachmentForm, SuratForm
from .models import Surat, SuratAttachment
from .services import generate_nomor_surat


@login_required
def dashboard(request):
    """Main dashboard with statistics and recent documents."""
    total = Surat.objects.count()
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
        'total': total,
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
    form = SuratForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        surat = form.save(commit=False)
        surat.created_by = request.user
        surat.nomor_surat = generate_nomor_surat(
            surat.jenis_naskah, surat.klasifikasi, request.user,
        )
        surat.save()

        # Handle file attachments
        files = request.FILES.getlist('attachments')
        for f in files:
            SuratAttachment.objects.create(
                surat=surat,
                file=f,
                filename=f.name,
            )

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
    """Update a document (only if still in draft)."""
    surat = get_object_or_404(Surat, pk=pk)
    if not surat.is_editable:
        messages.error(request, 'Surat tidak dapat diedit karena sudah diajukan.')
        return redirect('surat:surat_detail', pk=pk)

    form = SuratForm(request.POST or None, instance=surat)
    if request.method == 'POST' and form.is_valid():
        form.save()

        # Handle new file attachments
        files = request.FILES.getlist('attachments')
        for f in files:
            SuratAttachment.objects.create(
                surat=surat,
                file=f,
                filename=f.name,
            )

        messages.success(request, 'Surat berhasil diperbarui.')
        return redirect('surat:surat_detail', pk=pk)

    attachments = surat.attachments.all()
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
