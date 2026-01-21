from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    IS_PATIENT = 'patient'
    IS_DOCTOR = 'doctor'
    IS_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (IS_PATIENT, 'Patient'),
        (IS_DOCTOR, 'Doctor'),
        (IS_ADMIN, 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=IS_PATIENT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_approved = models.BooleanField(default=True) # Default True for patients/admins

    def __str__(self):
        return f"{self.username} ({self.role})"
 