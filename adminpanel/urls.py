from django.urls import path
from . import views
app_name = 'adminpanel'
urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('users/', views.manage_users, name='manage_users'),
    path('facilities/', views.manage_facilities, name='manage_facilities'),
    path('pending_approvals/', views.pending_approvals, name='pending_approvals'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
]
