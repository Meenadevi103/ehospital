from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   # role already saved here

            #login(request, user)
            if user.role == 'doctor':
                messages.info(request, "Registration successful! Your account is pending administrator approval. Once accepted, you can login.")
            else:
                messages.success(request, f"Registration successful as {user.role}. Welcome, {user.username}!")
            
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
@login_required
def role_redirect(request):
    user = request.user
    
    if not user.is_approved:
        from django.contrib.auth import logout
        logout(request)
        messages.error(request, "Your account is pending administrator approval.")
        return redirect('login')

    if user.role == 'patient':
        return redirect('patient_dashboard')

    elif user.role == 'doctor':
        return redirect('doctor_dashboard')

    elif user.role == 'admin':
        return redirect('admin_dashboard')

    elif user.is_superuser:
        return redirect('/admin/')

    else:
        return redirect('index')
