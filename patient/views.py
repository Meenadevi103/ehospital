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
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
def medical_records(request):
    if request.user.role != 'patient':
        return redirect('index')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    history = MedicalHistory.objects.filter(patient=profile).order_by('-record_date')
    
    return render(request, 'patient/medical_records.html', {
        'history': history,
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
