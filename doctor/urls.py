from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('prescribe/<int:appointment_id>/', views.prescription_create, name='create_prescription'),
    path('patient/<int:patient_id>/', views.patient_details, name='patient_details'),
]
