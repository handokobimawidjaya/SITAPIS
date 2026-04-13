"""
Forms for the accounts app: authentication and user management.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    """Custom login form with styled widgets."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )


class UserForm(forms.ModelForm):
    """Form for creating and editing users."""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        }),
        required=True,
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Konfirmasi Password',
        }),
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'satker', 'sub_bagian', 'phone', 'avatar', 'is_active',
        ]
        labels = {
            'username': 'Nama Pengguna',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'email': 'Alamat Email',
            'role': 'Role',
            'satker': 'Satuan Kerja',
            'sub_bagian': 'Sub Bagian',
            'phone': 'Telepon',
            'avatar': 'Foto Profil',
            'is_active': 'Aktif',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'satker': forms.Select(attrs={'class': 'form-input'}),
            'sub_bagian': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        """Add required attribute to mandatory fields."""
        super().__init__(*args, **kwargs)
        # Set required fields
        required_fields = ['username', 'first_name', 'email', 'role', 'satker', 'phone']
        
        # Password is only required when creating a new user
        if not self.instance.pk:
            required_fields.extend(['password1', 'password2'])
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        else:
            # When editing, passwords are optional
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].label = 'Password Baru (opsional)'
            self.fields['password2'].label = 'Konfirmasi Password Baru (opsional)'
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                # Add required attribute to widget for HTML5 validation
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True

    def clean(self):
        """Validate that both password fields match and are provided."""
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        
        # Only require passwords when creating a new user
        if not self.instance.pk:
            if not p1 and not p2:
                raise forms.ValidationError('Password wajib diisi.')
        
        # If either password is provided, they must match
        if p1 or p2:
            if p1 and not p2:
                self.add_error('password2', 'Konfirmasi Password Baru wajib diisi jika Anda mengisi Password Baru.')
            elif not p1 and p2:
                self.add_error('password1', 'Password Baru wajib diisi jika Anda mengisi Konfirmasi Password.')
            elif p1 != p2:
                self.add_error('password2', 'Password tidak cocok.')
        
        return cleaned

    def save(self, commit=True):
        """Save user and set password if provided."""
        user = super().save(commit=False)
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Form for users editing their own profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
        }
