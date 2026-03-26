"""
Views for the approval workflow app.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import role_required
from apps.surat.models import Surat

from .models import ApprovalHistory


@login_required
def submit_surat(request, pk):
    """Submit a draft document for approval."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.DRAFT:
        messages.error(request, 'Surat ini tidak dalam status draft.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        surat.status = Surat.Status.SUBMITTED
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.SUBMIT,
            user=request.user,
            comment=request.POST.get('comment', ''),
        )
        messages.success(request, 'Surat berhasil diajukan untuk approval.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
@role_required('admin', 'manager')
def approve_surat(request, pk):
    """Approve a submitted document. Manager or admin only."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.SUBMITTED:
        messages.error(request, 'Surat ini tidak dalam status diajukan.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        surat.status = Surat.Status.APPROVED
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.APPROVE,
            user=request.user,
            comment=request.POST.get('comment', ''),
        )
        messages.success(request, 'Surat berhasil disetujui.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
@role_required('admin', 'manager')
def reject_surat(request, pk):
    """Reject a submitted document. Manager or admin only."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.SUBMITTED:
        messages.error(request, 'Surat ini tidak dalam status diajukan.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        if not comment:
            messages.error(request, 'Wajib memberikan alasan penolakan.')
            return redirect('surat:surat_detail', pk=pk)

        surat.status = Surat.Status.REJECTED
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.REJECT,
            user=request.user,
            comment=comment,
        )
        messages.warning(request, 'Surat ditolak.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
def revise_surat(request, pk):
    """Revise a rejected document back to draft for re-submission."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.REJECTED:
        messages.error(request, 'Hanya surat yang ditolak yang dapat direvisi.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        surat.status = Surat.Status.DRAFT
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.REVISE,
            user=request.user,
            comment=request.POST.get('comment', ''),
        )
        messages.info(request, 'Surat dikembalikan ke draft untuk revisi.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
def approval_list(request):
    """List documents pending approval."""
    pending = Surat.objects.filter(
        status=Surat.Status.SUBMITTED,
    ).select_related('jenis_naskah', 'klasifikasi', 'created_by').order_by('-created_at')

    return render(request, 'approval/approval_list.html', {
        'pending': pending,
    })
