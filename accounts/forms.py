from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class   PatientRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'age',
            'gender',
            'phone',
            'password1',
            'password2'
        ]
class DoctorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'department',
            'qualification',
            'experience',
            'availability',
            'password1',
            'password2'
        ]