from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.patient_register, name='patient_register'),
    path('login/', views.custom_login, name='login'),
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('admin/add-doctor/', views.add_doctor, name='add_doctor'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  

]
