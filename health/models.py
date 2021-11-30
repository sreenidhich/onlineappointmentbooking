from django.db import models
from django.contrib.auth.models import User
# Create your models here.
blood_group=[('-A','-A'),
('+A','+A'),
('-B','-B'),
('+B','+B'),
('-AB','-AB'),
('+AB','+AB'),
('-O','-O'),
('+O','+O'),
]
gender=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]
class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blood_group = models.CharField(max_length=10,choices=blood_group,null=True)
   
    ex_year= models.CharField(max_length=10,null=True)
    ex_month= models.CharField(max_length=10,null=True)
   
    mobile = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=100,null=True)
   
    dob = models.DateField(null=True)

    def __str__(self):
        return self.user.username
class Doctor(models.Model):
    status = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    specialist = models.CharField(max_length=100, null=True)    
    daystiming = models.CharField(max_length=100, null=True)
    timing = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=100,choices=gender,null=True)
    biography = models.TextField(null=True)
    
    def __str__(self):
        return self.user.username
        
class Appointment(models.Model):
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    
    a_date=models.DateField(null=True)
    a_timing=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    p_status=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.doctor.user.username+" has an appointment with " +self.patient.user.username
class Adminstration(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.user.username


