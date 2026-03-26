"""
URL configuration for the surat (document) app.
"""

from django.urls import path

from . import views

app_name = 'surat'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('surat/', views.surat_list, name='surat_list'),
    path('surat/create/', views.surat_create, name='surat_create'),
    path('surat/<int:pk>/', views.surat_detail, name='surat_detail'),
    path('surat/<int:pk>/edit/', views.surat_update, name='surat_update'),
    path('surat/<int:pk>/delete/', views.surat_delete, name='surat_delete'),
    path('attachment/<int:pk>/delete/', views.attachment_delete, name='attachment_delete'),
]
