from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('records/', views.medical_records, name='medical_records'),
    path('billing/', views.billing_list, name='billing_list'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('payment/<int:billing_id>/', views.payment, name='payment'),
]
