"""
Views for the approval workflow app.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import role_required
from apps.accounts.models import User
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
        # For "terkini" category, auto-approve through all levels
        if surat.kategori_surat == 'terkini':
            surat.status = Surat.Status.APPROVED
            surat.save(update_fields=['status'])

            ApprovalHistory.objects.create(
                surat=surat,
                action=ApprovalHistory.Action.APPROVE,
                user=request.user,
                comment='',
            )
            messages.success(request, 'Surat berhasil diajukan dan langsung disetujui.')
        else:
            # For "urgensi", submit to Kasubbag approval first
            surat.status = Surat.Status.SUBMITTED
            surat.save(update_fields=['status'])

            ApprovalHistory.objects.create(
                surat=surat,
                action=ApprovalHistory.Action.SUBMIT,
                user=request.user,
                comment=request.POST.get('comment', ''),
            )
            messages.success(request, 'Surat berhasil diajukan untuk approval Kasubbag.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
@role_required('admin', 'kasubbag', 'sekretaris')
def approve_surat(request, pk):
    """Approve a submitted document. Kasubbag or Sekretaris or Admin only."""
    surat = get_object_or_404(Surat, pk=pk)

    if request.method == 'POST':
        # Kasubbag approval (submitted → approved_kasubbag)
        if surat.status == Surat.Status.SUBMITTED:
            if request.user.role not in [User.Role.ADMIN, User.Role.KASUBBAG]:
                messages.error(request, 'Anda tidak memiliki wewenang untuk menyetujui surat ini.')
                return redirect('surat:surat_detail', pk=pk)
                
            surat.status = Surat.Status.APPROVED_KASUBBAG
            surat.save(update_fields=['status'])
            
            ApprovalHistory.objects.create(
                surat=surat,
                action=ApprovalHistory.Action.APPROVE,
                user=request.user,
                comment=request.POST.get('comment', ''),
            )
            messages.success(request, 'Surat berhasil disetujui Kasubbag. Menunggu approval Sekretaris.')
            
        # Sekretaris approval (approved_kasubbag → approved)
        elif surat.status == Surat.Status.APPROVED_KASUBBAG:
            if request.user.role not in [User.Role.ADMIN, User.Role.SEKRETARIS]:
                messages.error(request, 'Anda tidak memiliki wewenang untuk menyetujui surat ini.')
                return redirect('surat:surat_detail', pk=pk)
                
            surat.status = Surat.Status.APPROVED
            surat.save(update_fields=['status'])
            
            ApprovalHistory.objects.create(
                surat=surat,
                action=ApprovalHistory.Action.APPROVE,
                user=request.user,
                comment=request.POST.get('comment', ''),
            )
            messages.success(request, 'Surat berhasil disetujui Sekretaris. Silakan upload lampiran.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
@role_required('admin', 'kasubbag', 'sekretaris')
def reject_surat(request, pk):
    """Reject a submitted document. Kasubbag or Sekretaris or Admin only."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status not in [Surat.Status.SUBMITTED, Surat.Status.APPROVED_KASUBBAG]:
        messages.error(request, 'Surat ini tidak dalam status untuk ditolak.')
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
def start_surat(request, pk):
    """Start working on approved surat (change from APPROVED to INPROGRESS)."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.APPROVED:
        messages.error(request, 'Surat ini sudah diproses.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        surat.status = Surat.Status.INPROGRESS
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.INPROGRESS,
            user=request.user,
            comment='Mulai mengerjakan dan menindak lanjuti surat',
        )
        messages.info(request, 'Silakan upload lampiran untuk menyelesaikan surat.')

    return redirect('surat:surat_detail', pk=pk)


@login_required
def complete_surat(request, pk):
    """Complete surat by uploading attachment (change from INPROGRESS to DONE)."""
    surat = get_object_or_404(Surat, pk=pk)

    if surat.status != Surat.Status.INPROGRESS:
        messages.error(request, 'Surat ini tidak dapat diselesaikan.')
        return redirect('surat:surat_detail', pk=pk)

    if request.method == 'POST':
        # Check if attachment is uploaded
        files = request.FILES.getlist('attachments')
        if not files:
            messages.error(request, 'Wajib upload lampiran untuk menyelesaikan surat.')
            return redirect('surat:surat_detail', pk=pk)

        # Save attachments
        for f in files:
            from apps.surat.models import SuratAttachment
            SuratAttachment.objects.create(
                surat=surat,
                file=f,
                filename=f.name,
            )

        surat.status = Surat.Status.DONE
        surat.save(update_fields=['status'])

        ApprovalHistory.objects.create(
            surat=surat,
            action=ApprovalHistory.Action.APPROVE,
            user=request.user,
            comment='Lampiran diupload, surat selesai',
        )
        messages.success(request, 'Surat berhasil diselesaikan.')

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
