from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    specialization = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Neurology, Cardiology, etc.'}))
    experience_years = forms.IntegerField(required=False, min_value=0, initial=0)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email', 'phone_number')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        
        # New: Set is_approved to False for doctors
        if user.role == User.IS_DOCTOR:
            user.is_approved = False
        else:
            user.is_approved = True
            
        if commit:
            user.save()
            # Create DoctorProfile if role is doctor
            if user.role == User.IS_DOCTOR:
                from doctor.models import DoctorProfile
                DoctorProfile.objects.create(
                    user=user,
                    specialization=self.cleaned_data.get('specialization', 'General'),
                    experience_years=self.cleaned_data.get('experience_years', 0)
                )
        return user
