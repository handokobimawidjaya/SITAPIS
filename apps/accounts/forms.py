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
        required=False,
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Konfirmasi Password',
        }),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'satker', 'phone', 'avatar', 'is_active',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'satker': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean(self):
        """Validate that both password fields match."""
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError('Password tidak cocok.')
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
