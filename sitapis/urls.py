"""
SITAPIS URL Configuration.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.surat.urls', namespace='surat')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('master/', include('apps.master.urls', namespace='master')),
    path('approval/', include('apps.approval.urls', namespace='approval')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
