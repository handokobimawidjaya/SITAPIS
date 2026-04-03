"""
Forms for the surat (document) app.
"""

from django import forms

from apps.master.models import JenisNaskahDinas, KlasifikasiArsip

from .models import Surat, SuratAttachment, SuratMasuk


class SuratForm(forms.ModelForm):
    """
    Form for creating and editing documents/letters.

    User selects Jenis Naskah Dinas and Klasifikasi Arsip.
    SATKER is auto-detected from the user's account.
    """

    jenis_naskah = forms.ModelChoiceField(
        queryset=JenisNaskahDinas.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Jenis Naskah Dinas',
    )
    klasifikasi = forms.ModelChoiceField(
        queryset=KlasifikasiArsip.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Klasifikasi Arsip',
    )
    kategori_surat = forms.ChoiceField(
        choices=[('urgensi', 'Urgensi'), ('terkini', 'Terkini')],
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Kategori Surat',
        initial='terkini',
    )

    class Meta:
        model = Surat
        fields = [
            'jenis_naskah', 'klasifikasi', 'kategori_surat', 'perihal', 'tanggal',
            'tujuan', 'pengirim', 'notes',
        ]
        widgets = {
            'perihal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Perihal surat',
                'required': 'required',
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': 'required',
            }),
            'tujuan': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tujuan surat',
                'required': 'required',
            }),
            'pengirim': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama pengirim',
                'required': 'required',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Catatan tambahan...',
            }),
        }

    def clean(self):
        """Validate form based on kategori_surat."""
        cleaned_data = super().clean()
        kategori = cleaned_data.get('kategori_surat')
        notes = cleaned_data.get('notes')

        if kategori == 'urgensi' and not notes:
            raise forms.ValidationError('Catatan wajib diisi untuk surat Urgensi.')

        return cleaned_data


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


from django.contrib.auth import get_user_model
User = get_user_model()

class SuratMasukForm(forms.ModelForm):
    """
    Form for creating and editing Surat Masuk.
    Only allows disposisi to users with role 'kasubbag' or 'sekretaris'.
    """

    disposisi = forms.ModelChoiceField(
        queryset=User.objects.filter(role__in=[User.Role.KASUBBAG, User.Role.SEKRETARIS], is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Disposisi Ke',
        empty_label='--- Pilih Karyawan ---',
    )

    class Meta:
        model = SuratMasuk
        fields = [
            'nomor_surat', 'pengirim', 'perihal', 'disposisi', 'lampiran_surat'
        ]
        widgets = {
            'nomor_surat': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nomor surat masuk',
                'required': 'required',
            }),
            'pengirim': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama instansi pengirim',
                'required': 'required',
            }),
            'perihal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Perihal surat',
                'required': 'required',
            }),
            'lampiran_surat': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf',
            }),
        }


class SuratMasukTindakLanjutForm(forms.ModelForm):
    """
    Form for completing a Surat Masuk disposition (Inprogress -> Done).
    """

    class Meta:
        model = SuratMasuk
        fields = ['catatan']
        widgets = {
            'catatan': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Beri alasan atau komentar tindak lanjut penyelesaian surat...',
                'required': 'required',
            }),
        }
