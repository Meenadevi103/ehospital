from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class PatientRegistrationForm(UserCreationForm):

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
    # Add name fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Doctor\'s first name'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Doctor\'s last name'
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })