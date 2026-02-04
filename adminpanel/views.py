from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Department, Facility
from patient.models import Appointment
from django.contrib import messages
from accounts.forms import DoctorCreationForm

@login_required
def dashboard(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('index')

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


@login_required
def add_doctor(request):

    # Only admin or superuser allowed
    if not (request.user.role == 'admin' or request.user.is_superuser):
        messages.error(request, "Unauthorized Access")
        return redirect('index')

    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.role = 'doctor'
            doctor.is_approved = True
            doctor.save()

            messages.success(request, "Doctor added successfully!")
            return redirect('adminpanel:admin_dashboard')
    else:
        form = DoctorCreationForm()

    return render(request, 'adminpanel/add_doctor.html', {'form': form})

@login_required
def pending_approvals(request):
    if (request.user.role != 'admin' or request.user.is_superuser):
        return redirect('index')
    
    pending_doctors = User.objects.filter(role='doctor', is_approved=False)
    return render(request, 'adminpanel/pending_approvals.html', {'doctors': pending_doctors})

@login_required
def approve_user(request, user_id):
    if (request.user.role != 'admin' or request.user.is_superuser):
        return redirect('index')
    
    doctor = User.objects.get(id=user_id)
    doctor.is_approved = True
    doctor.save()
    from django.contrib import messages
    messages.success(request, f"Dr. {doctor.username} has been approved.")
    return redirect('adminpanel:pending_approvals')

@login_required
def manage_users(request):
    if (request.user.role != 'admin'or request.user.is_superuser):
        return redirect('index')
    
    users = User.objects.all()
    return render(request, 'adminpanel/manage_users.html', {'users': users})

@login_required
def manage_facilities(request):
    if (request.user.role != 'admin' or request.user.is_superuser):
        return redirect('index')
    
    facilities = Facility.objects.all()
    return render(request, 'adminpanel/manage_facilities.html', {'facilities': facilities})
