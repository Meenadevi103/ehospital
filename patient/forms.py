from django import forms
from .models import PatientProfile, Appointment

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'address', 'blood_group']

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from doctor.models import DoctorProfile
        # Only show doctors who are approved
        self.fields['doctor'].queryset = DoctorProfile.objects.filter(
            user__is_approved=True
        ).select_related('user').order_by('user__first_name', 'user__last_name')
        
        # Display doctor with their full name and specialization
        self.fields['doctor'].label_from_instance = lambda obj: (
            f"Dr. {obj.user.first_name} {obj.user.last_name} - {obj.specialization}"
        )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
        }
