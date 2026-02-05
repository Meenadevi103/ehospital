from django.shortcuts import render, redirect
from .models import DoctorProfile

from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, Prescription
from patient.models import Appointment, PatientProfile, MedicalHistory
from datetime import date

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('index')
    
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)
    
    # Get appointments for this doctor for today with patient information
    today = date.today()
    appointments = Appointment.objects.filter(
        doctor=profile,
        appointment_date__date=today
    ).order_by('appointment_date').select_related('patient__user')
    
    context = {
        'profile': profile,
        'appointments': appointments,
    }
    return render(request, 'doctor/dashboard.html', context)

@login_required
def prescription_create(request, appointment_id):
    if request.user.role != 'doctor':
        return redirect('index')
    
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        # Simple e-prescribing logic
        medication = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')
        
        Prescription.objects.create(
            doctor=request.user.doctor_profile,
            patient=appointment.patient,
            medication_name=medication,
            dosage=dosage,
            instructions=instructions
        )
        appointment.status = 'Completed'
        appointment.save()
        return redirect('doctor_dashboard')
    
    return render(request, 'doctor/create_prescription.html', {'appointment': appointment})

@login_required
def patient_details(request, patient_id):
    if request.user.role != 'doctor':
        return redirect('index')
    
    patient = PatientProfile.objects.get(id=patient_id)
    history = MedicalHistory.objects.filter(patient=patient).order_by('-record_date')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-prescribed_date')
    
    return render(request, 'doctor/patient_details.html', {
        'patient': patient,
        'history': history,
        'prescriptions': prescriptions
    })
