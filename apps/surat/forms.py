"""
Forms for the surat (document) app.
"""

from django import forms

from apps.master.models import JenisNaskahDinas, KlasifikasiArsip

from .models import Surat, SuratAttachment


class SuratForm(forms.ModelForm):
    """
    Form for creating and editing documents/letters.

    User selects Jenis Naskah Dinas and Klasifikasi Arsip.
    SATKER is auto-detected from the user's account.
    """

    jenis_naskah = forms.ModelChoiceField(
        queryset=JenisNaskahDinas.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Jenis Naskah Dinas',
    )
    klasifikasi = forms.ModelChoiceField(
        queryset=KlasifikasiArsip.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Klasifikasi Arsip',
    )

    class Meta:
        model = Surat
        fields = [
            'jenis_naskah', 'klasifikasi', 'perihal', 'tanggal',
            'tujuan', 'pengirim', 'notes',
        ]
        widgets = {
            'perihal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Perihal surat',
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'tujuan': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tujuan surat',
            }),
            'pengirim': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama pengirim',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Catatan tambahan...',
            }),
        }


class SuratAttachmentForm(forms.ModelForm):
    """Form for uploading file attachments."""

    class Meta:
        model = SuratAttachment
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.png,.zip',
            }),
        }
