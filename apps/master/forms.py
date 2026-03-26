"""
Forms for the master data app.
"""

from django import forms

from .models import (
    JenisNaskahDinas,
    KlasifikasiArsip,
    UnitKerja,
)


class KlasifikasiArsipForm(forms.ModelForm):
    """Form for creating and editing archive classification codes."""

    class Meta:
        model = KlasifikasiArsip
        fields = ['kode', 'nama', 'deskripsi', 'jenis', 'parent', 'is_active']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'jenis': forms.Select(attrs={'class': 'form-input'}),
            'parent': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class JenisNaskahDinasForm(forms.ModelForm):
    """Form for creating and editing letter type codes."""

    class Meta:
        model = JenisNaskahDinas
        fields = ['kode', 'nama', 'is_active']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class UnitKerjaForm(forms.ModelForm):
    """Form for creating and editing organizational units."""

    class Meta:
        model = UnitKerja
        fields = ['kode', 'nama', 'is_active']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
