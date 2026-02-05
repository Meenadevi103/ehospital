from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
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
            user.role = 'patient'
            user.is_approved = True
            user.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patient/patient_register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # coming from hidden input

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # ❌ Doctor trying to login from wrong page
            if user.role == 'doctor':
                messages.error(request, "Doctors must login from Doctor Login page.")
                return redirect('login')

            # 🔐 Admin Login Box
            if role == 'admin':
                if not (user.role == 'admin' or user.is_superuser):
                    messages.error(request, "Access denied. Admins only.")
                    return redirect('login')

            # 👤 Patient Login Box
            elif role == 'patient':
                if user.role != 'patient':
                    messages.error(request, "Access denied. Patients only.")
                    return redirect('login')

            login(request, user)
            return redirect('role_redirect')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')



# 🩺 Doctor Login (Separate)
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.role != 'doctor':
                messages.error(request, "Access Denied! Doctors only.")
                return redirect('doctor_login')

            if not user.is_approved:
                messages.error(request, "Your account is not approved yet.")
                return redirect('doctor_login')

            login(request, user)
            return redirect('doctor_dashboard')

        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'doctor/doctor_login.html')


@login_required
def role_redirect(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
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
    if request.user.role != 'admin':
        messages.error(request, "Unauthorized Access")
        return redirect('index')

    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            doctor.role = 'doctor'
            doctor.is_approved = True
            doctor.save()

            messages.success(request, "Doctor added successfully!")
            return redirect('admin_dashboard')
    else:
        form = DoctorCreationForm()

    return render(request, 'accounts/add_doctor.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('index')

    from adminpanel.models import Department
    from patient.models import Appointment

    context = {
        'users_count': User.objects.count(),
        'patients_count': User.objects.filter(role='patient').count(),
        'doctors_count': User.objects.filter(role='doctor').count(),
        'total_appointments': Appointment.objects.count(),
        'pending_count': User.objects.filter(role='doctor', is_approved=False).count(),
        'recent_users': User.objects.all().order_by('-date_joined')[:5],
        'departments': Department.objects.all(),
    }

    return render(request, 'adminpanel/dashboard.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')
