from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['blood_group','mobile','address','dob']
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['experience','specialist','daystiming','timing','gender','biography','mobile','address','dob']
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['a_date','a_timing','status','p_status']


