from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile, Appointment, MedicalHistory, Billing, HealthResource
from .forms import PatientProfileForm, AppointmentForm

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('index')
    
    # Get or create profile
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    appointments = Appointment.objects.filter(patient=profile).order_by('-appointment_date')
    history = MedicalHistory.objects.filter(patient=profile).order_by('-record_date')
    billings = Billing.objects.filter(patient=profile).order_by('-billing_date')
    resources = HealthResource.objects.all()[:5]
    
    context = {
        'profile': profile,
        'appointments': appointments,
        'history': history,
        'billings': billings,
        'resources': resources,
    }
    return render(request, 'patient/dashboard.html', context)

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = profile
            appointment.save()
            
            # Create billing record for appointment
            billing = Billing.objects.create(
                patient=profile,
                amount=50.00,
                status='Unpaid'
            )
            
            # Redirect to payment page
            return redirect('payment', billing_id=billing.id)
    else:
        form = AppointmentForm()
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
def medical_records(request):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    history = MedicalHistory.objects.filter(patient=profile).order_by('-record_date')
    
    # Import Prescription model to get prescriptions
    from doctor.models import Prescription
    prescriptions = Prescription.objects.filter(patient=profile).order_by('-prescribed_date')
    
    return render(request, 'patient/medical_records.html', {
        'history': history,
        'prescriptions': prescriptions,
        'profile': profile
    })

@login_required
def billing_list(request):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    billings = Billing.objects.filter(patient=profile).order_by('-billing_date')
    
    return render(request, 'patient/billing_list.html', {
        'billings': billings,
        'profile': profile
    })

@login_required
def cancel_appointment(request, appointment_id):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    appointment = Appointment.objects.get(id=appointment_id, patient=profile)
    
    if appointment.status != 'Cancelled':
        appointment.status = 'Cancelled'
        appointment.save()
    
    return redirect('patient_dashboard')

@login_required
def payment(request, billing_id):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    billing = Billing.objects.get(id=billing_id, patient=profile)
    
    if request.method == 'POST':
        # Process payment
        billing.status = 'Paid'
        billing.save()
        return redirect('billing_list')
    
    return render(request, 'patient/payment.html', {
        'billing': billing,
        'profile': profile
    })
