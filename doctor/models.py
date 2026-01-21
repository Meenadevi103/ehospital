from django.db import models
from django.conf import settings

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    #consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=100, default="Mon-Fri", blank=True) # e.g. "Mon, Wed, Fri"
    department = models.ForeignKey('adminpanel.Department', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"

class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.PatientProfile', on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    prescribed_date = models.DateTimeField(auto_now_add=True)
