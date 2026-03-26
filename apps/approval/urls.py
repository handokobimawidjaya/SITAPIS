"""
URL configuration for the approval workflow app.
"""

from django.urls import path

from . import views

app_name = 'approval'

urlpatterns = [
    path('', views.approval_list, name='approval_list'),
    path('submit/<int:pk>/', views.submit_surat, name='submit'),
    path('approve/<int:pk>/', views.approve_surat, name='approve'),
    path('reject/<int:pk>/', views.reject_surat, name='reject'),
    path('revise/<int:pk>/', views.revise_surat, name='revise'),
]
