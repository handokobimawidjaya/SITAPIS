"""
Forms for the surat (document) app.
"""

from django import forms

from apps.master.models import JenisNaskahDinas, KlasifikasiArsip, SubBagian

from .models import Surat, SuratAttachment, SuratMasuk


class SuratForm(forms.ModelForm):
    """
    Form for creating and editing documents/letters.

    User selects Jenis Naskah Dinas and Klasifikasi Arsip.
    SATKER is auto-detected from the user's account.
    """

    # 1. Jenis Naskah Dinas
    jenis_naskah = forms.ModelChoiceField(
        queryset=JenisNaskahDinas.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Jenis Naskah Dinas',
        empty_label='----------',
    )
    # 2. Klasifikasi Arsip
    klasifikasi = forms.ModelChoiceField(
        queryset=KlasifikasiArsip.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Klasifikasi Arsip',
        empty_label='----------',
    )
    # 3. Tujuan Surat
    tujuan_surat = forms.ChoiceField(
        choices=[('external', 'External'), ('internal', 'Internal')],
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required', 'id': 'id_tujuan_surat'}),
        label='Tujuan Surat',
        initial='external',
    )
    # 4. Sub Bagian (visible only when Internal)
    sub_bagian = forms.ModelChoiceField(
        queryset=SubBagian.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'id_sub_bagian'}),
        label='Sub Bagian',
        empty_label='--- Pilih Sub Bagian ---',
        required=False,
    )
    # 5. Kategori Surat
    kategori_surat = forms.ChoiceField(
        choices=[('terkini', 'Terkini'), ('urgensi', 'Urgensi')],
        widget=forms.Select(attrs={'class': 'form-input', 'required': 'required'}),
        label='Kategori Surat',
        initial='terkini',
    )
    # 6. Perihal
    perihal = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Perihal surat',
            'required': 'required',
        }),
        label='Perihal',
    )
    # 7. Tanggal Surat
    tanggal = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'required': 'required',
        }),
        label='Tanggal Surat',
    )
    # 8. Penerima
    penerima = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nama penerima surat',
        }),
        label='Penerima',
        required=False,
    )
    # 9. Pengirim
    pengirim = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nama pengirim',
        }),
        label='Pengirim',
        required=False,
    )
    # 10. Catatan
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 3,
            'placeholder': 'Catatan tambahan...',
        }),
        label='Catatan',
        required=False,
    )

    class Meta:
        model = Surat
        fields = [
            'jenis_naskah', 'klasifikasi', 'tujuan_surat', 'sub_bagian',
            'kategori_surat', 'perihal', 'tanggal', 'penerima', 'pengirim', 'notes',
        ]

    def clean(self):
        """Validate form based on kategori_surat and tujuan_surat."""
        cleaned_data = super().clean()
        kategori = cleaned_data.get('kategori_surat')
        notes = cleaned_data.get('notes')
        tujuan_surat = cleaned_data.get('tujuan_surat')
        sub_bagian = cleaned_data.get('sub_bagian')

        if kategori == 'urgensi' and not notes:
            raise forms.ValidationError('Catatan wajib diisi untuk surat Urgensi.')

        # Sub Bagian is required when Tujuan Surat is Internal
        if tujuan_surat == 'internal' and not sub_bagian:
            raise forms.ValidationError('Sub Bagian wajib diisi untuk surat Internal.')

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
