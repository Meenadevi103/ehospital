from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import PatientRegistrationForm, DoctorCreationForm
from .models import User


def index(request):
    return render(request, 'index.html')


# 👤 Patient Registration
def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'patient'      # Force patient role
            user.is_approved = True    # Patients auto approved
            user.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patient/patient_register.html', {'form': form})

@login_required
def role_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('adminpanel:admin_dashboard')

    if not user.is_approved:
        logout(request)
        messages.error(request, "Your account is pending admin approval.")
        return redirect('login')

    if user.role == 'admin':
        return redirect('adminpanel:admin_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    elif user.role == 'doctor':
        return redirect('doctor_dashboard')
    else:
        return redirect('index')



# 🩺 Admin Adds Doctor
@login_required
def add_doctor(request):

    # Only admin allowed
    if request.user.role != 'admin':
        messages.error(request, "Unauthorized Access")
        return redirect('index')

    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.role = 'doctor'
            doctor.is_approved = True  # Admin-created doctor is approved
            doctor.save()

            messages.success(request, "Doctor added successfully!")
            return redirect('admin_dashboard')
    else:
        form = DoctorCreationForm()

    return render(request, 'accounts/add_doctor.html', {'form': form})


@login_required
def admin_dashboard(request):

    # SUPERUSER always allowed
    if request.user.is_superuser:
        pass

    # Normal admin role allowed
    elif request.user.role == 'admin':
        pass

    else:
        return redirect('index')

    from adminpanel.models import Department, Facility
    from patient.models import Appointment

    users_count = User.objects.count()
    patients_count = User.objects.filter(role='patient').count()
    doctors_count = User.objects.filter(role='doctor').count()
    total_appointments = Appointment.objects.count()
    pending_count = User.objects.filter(role='doctor', is_approved=False).count()

    recent_users = User.objects.all().order_by('-date_joined')[:5]
    departments = Department.objects.all()

    context = {
        'users_count': users_count,
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'total_appointments': total_appointments,
        'pending_count': pending_count,
        'recent_users': recent_users,
        'departments': departments,
    }
    return render(request, 'adminpanel/dashboard.html', context)



def logout_view(request):
    logout(request)  # Ends session
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')