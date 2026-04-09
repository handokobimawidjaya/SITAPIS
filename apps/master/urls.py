"""
URL configuration for the master data app.
"""

from django.urls import path

from . import views

app_name = 'master'

urlpatterns = [
    # Klasifikasi Arsip
    path('klasifikasi/', views.klasifikasi_arsip_list, name='klasifikasi_arsip_list'),
    path('klasifikasi/create/', views.klasifikasi_arsip_create, name='klasifikasi_arsip_create'),
    path('klasifikasi/<int:pk>/edit/', views.klasifikasi_arsip_update, name='klasifikasi_arsip_update'),
    path('klasifikasi/<int:pk>/delete/', views.klasifikasi_arsip_delete, name='klasifikasi_arsip_delete'),
    # Jenis Naskah Dinas
    path('jenis-naskah/', views.jenis_naskah_list, name='jenis_naskah_list'),
    path('jenis-naskah/create/', views.jenis_naskah_create, name='jenis_naskah_create'),
    path('jenis-naskah/<int:pk>/edit/', views.jenis_naskah_update, name='jenis_naskah_update'),
    path('jenis-naskah/<int:pk>/delete/', views.jenis_naskah_delete, name='jenis_naskah_delete'),
    # Unit Kerja
    path('unit-kerja/', views.unit_kerja_list, name='unit_kerja_list'),
    path('unit-kerja/create/', views.unit_kerja_create, name='unit_kerja_create'),
    path('unit-kerja/<int:pk>/edit/', views.unit_kerja_update, name='unit_kerja_update'),
    path('unit-kerja/<int:pk>/delete/', views.unit_kerja_delete, name='unit_kerja_delete'),
    # Sub Bagian
    path('sub-bagian/', views.sub_bagian_list, name='sub_bagian_list'),
    path('sub-bagian/create/', views.sub_bagian_create, name='sub_bagian_create'),
    path('sub-bagian/<int:pk>/edit/', views.sub_bagian_update, name='sub_bagian_update'),
    path('sub-bagian/<int:pk>/delete/', views.sub_bagian_delete, name='sub_bagian_delete'),
]
