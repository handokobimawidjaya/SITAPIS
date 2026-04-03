"""
Views for the accounts app: authentication and user management.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import LoginForm, ProfileForm, UserForm
from .models import User


def login_view(request):
    """Handle user login with custom styled form."""
    if request.user.is_authenticated:
        return redirect('surat:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
        return redirect('surat:dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """View and edit user's own profile."""
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profil berhasil diperbarui.')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
@role_required('admin')
def user_list(request):
    """List all users. Admin only."""
    users = User.objects.select_related('satker').all()
    query = request.GET.get('q', '')
    if query:
        users = users.filter(username__icontains=query)

    return render(request, 'accounts/user_list.html', {
        'users': users,
        'query': query,
    })


@login_required
@role_required('admin')
def user_create(request):
    """Create a new user. Admin only."""
    form = UserForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pengguna berhasil dibuat.')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': 'Tambah Pengguna',
    })


@login_required
@role_required('admin')
def user_update(request, pk):
    """Update an existing user. Admin only."""
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pengguna berhasil diperbarui.')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': f'Edit Pengguna: {user.username}',
        'edit_user': user,
    })
