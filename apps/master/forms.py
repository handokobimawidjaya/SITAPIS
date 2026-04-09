"""
Forms for the master data app.
"""

from django import forms

from .models import (
    JenisNaskahDinas,
    KlasifikasiArsip,
    SubBagian,
    UnitKerja,
)


class KlasifikasiArsipForm(forms.ModelForm):
    """Form for creating and editing archive classification codes."""

    class Meta:
        model = KlasifikasiArsip
        fields = ['kode', 'nama', 'deskripsi', 'is_active']
        labels = {
            'kode': 'Kode',
            'nama': 'Nama',
            'deskripsi': 'Deskripsi',
            'is_active': 'Aktif',
        }
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        """Add required attribute to mandatory fields."""
        super().__init__(*args, **kwargs)
        required_fields = ['kode', 'nama']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True


class JenisNaskahDinasForm(forms.ModelForm):
    """Form for creating and editing letter type codes."""

    class Meta:
        model = JenisNaskahDinas
        fields = ['kode', 'nama', 'is_active']
        labels = {
            'kode': 'Kode',
            'nama': 'Nama',
            'is_active': 'Aktif',
        }
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        """Add required attribute to mandatory fields."""
        super().__init__(*args, **kwargs)
        required_fields = ['kode', 'nama']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True


class UnitKerjaForm(forms.ModelForm):
    """Form for creating and editing organizational units."""

    class Meta:
        model = UnitKerja
        fields = ['kode', 'nama', 'is_active']
        labels = {
            'kode': 'Kode',
            'nama': 'Nama',
            'is_active': 'Aktif',
        }
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        """Add required attribute to mandatory fields."""
        super().__init__(*args, **kwargs)
        required_fields = ['kode', 'nama']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True


class SubBagianForm(forms.ModelForm):
    """Form for creating and editing Sub Bagian."""

    class Meta:
        model = SubBagian
        fields = ['kode', 'nama', 'is_active']
        labels = {
            'kode': 'Kode',
            'nama': 'Nama',
            'is_active': 'Aktif',
        }
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-input'}),
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        """Add required attribute to mandatory fields."""
        super().__init__(*args, **kwargs)
        required_fields = ['kode', 'nama']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True
