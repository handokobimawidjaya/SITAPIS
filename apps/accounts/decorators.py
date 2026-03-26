"""
Role-based access control decorators.
"""

from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decorator that restricts access to users with specified roles.

    Usage::

        @role_required('admin', 'manager')
        def my_view(request):
            ...

    Args:
        *roles: One or more role strings (e.g. 'admin', 'manager', 'staff').
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                return HttpResponseForbidden(
                    '<h3>403 — Anda tidak memiliki akses ke halaman ini.</h3>'
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
