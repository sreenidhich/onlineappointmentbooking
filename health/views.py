from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import *
import datetime
import uuid
import random
from django.db.models import Avg,Sum,Count,Min,Max
from django.views.generic import TemplateView
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import datetime
import json
import http.client
import requests
from django.views.decorators.cache import cache_control
# Create your views here.
def access(user):
    try:
        user = Doctor.objects.get(user=user)
        if user.status == "pending":
            return False
        else:
            return True
    except:
           pass
def home(request):
    try:
        user = User.objects.get(username=request.user)
        error = Patient.objects.get(user=user)
        return redirect('patient_dashboard')
    except:
        try:
            user = User.objects.get(username=request.user)
            error = Doctor.objects.get(user=user)
            return redirect('doctor_dashboard')
        except:
                try:
                        user = User.objects.get(username=request.user)
                        if user.is_staff:
                            return redirect('admin_dashboard')
                except:
                        pass
    
    return render(request,'index.html')
def Registeration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            m = request.POST['mode']
            if m == "Patient":
                Patient.objects.create(user=user)
            if m == "Doctor":
                Doctor.objects.create(user=user,status="pending")
            messages.success(request,'You have Registered Successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    d = {'form':form}
    return render(request,'register.html',d)
@cache_control(no_cache=True, must_revalidate=True)
def Login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in Successfully')
            return redirect('home')
        else:
            messages.success(request,'Invalid Credential')
            return redirect('login')
    return render(request,'login.html')
@cache_control(no_cache=True, must_revalidate=True)
def Logout(request):
    logout(request)
    messages.info(request,'You have logged out successfully')
    return redirect('login')
def patient_dashboard(request):
    if request.user.is_authenticated:
        pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
        d = {'data':pat}
        return render(request,'patient/patient_dashboard.html',d)
    else:
        messages.info(request,'You are not logged in')
        return redirect('login')
def all_doctor_appointment(request):
    pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/all_doctor_appointment.html',d)
def doctor_dashboard(request):
    tod = datetime.date.today()
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    pend = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    c = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user)).count()
    up = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date__gte=tod).exclude(a_date=tod)
    today = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date=tod)
    t_today = today.count()
    t_pending = pend.count()
    d = {'data': data, 'total': c, 'up': up, 'today': today,'t_today':t_today,'t_pending':t_pending}
    return render(request,'doctor/doctor_dashboard.html',d)
def Patient_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Patient.objects.get(user=user)
    form = PatientForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = PatientForm(request.POST,request.FILES,instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("patient_profile")
    d = {'form':form}
    return render(request,'patient/profile.html',d)
def Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'patient/change_password.html')
def Doctor_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Doctor.objects.get(user=user)
    form = DoctorForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = DoctorForm(request.POST or None,request.FILES or None, instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("doctor_profile")
    d = {'doc':pat,'form':form}
    return render(request,'doctor/profile.html',d)
def Doctor_Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'doctor/change_password.html')
def search_doctor(request):
    data = Doctor.objects.all()
    l = "All"
    g = "All"
    s = "All"
    if request.method == "POST":
        l = ""
        s = ""
        g = ""
        try:
            l = request.POST['location']
        except:
            pass
        try:
            g = request.POST['gender_type']
        except:
            pass
        try:
            s = request.POST['specialist']
        except:
            pass
        data = Doctor.objects.filter(gender__icontains=g,specialist__icontains=s)
    d={'data':data,'l':l,'g':g,'s':s}
    return render(request,'patient/search_doctor.html',d)
def appointment(request,pid):
    doctor=Doctor.objects.get(id=pid)
    if request.method == "POST":
        a = request.POST['a_date']
        app=Appointment.objects.create(doctor=doctor,patient=Patient.objects.get(user=request.user),a_date=a,status="pending",p_status="pending")
        template1 =render_to_string('patient/pemail_template.html',{'name':request.user.first_name,'doctor':doctor.user.first_name})
        email="healthicde@gmail.com"
        url="https://api.zoom.us/v2/users/{}/meetings".format(email)
        date=datetime.datetime(2022,7,5,13,30).strftime("%Y-%m-%d T%H:%M:%S")
        obj={"topic":"Test Booking","starttime":date,"duration":30,"password":"12345"}
        mheader={"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjVRbVZWX2c4Um1xSmgySElOY0w4VEEiLCJleHAiOjE2Mzg2ODM3MDUsImlhdCI6MTYzODA3ODkwNn0.DLJ5wLRHtZwf_5vfeSxXc7S6xbg_BI1MoNj1Y3y7b70"}
        create_meeting=requests.post(url,json=obj,headers=mheader)
        final=create_meeting.text

        data_dict = json.loads(final)
        zoom_link= data_dict["start_url"]
        email = EmailMessage(
        'Appointment Confirmation',
        ''+ template1+ 'Kindly be present for the appointment with your Health card and ID Proof. Your appointmet link is as follows: ' + zoom_link ,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        )
        email.fail_silently=False
        email.send()
        return redirect("requestAppointment",app.id)
    d={'doctor':doctor}
    return render(request,'patient/appointment.html',d)
def requestAppointment(request,pid):
    data=Appointment.objects.get(id=pid)
    if request.method=="POST":
        data.p_status="complete"
        data.save()
        return render(request,'patient/requestAppointment.html',data.id)
    d={'data':data}
    return render(request,'patient/requestAppointment.html',d)
def p_appointment(request):
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="pending")
    d={'data':data}
    return render(request,'patient/p_appoinment.html',d)
def d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    d={'data':data}
    return render(request,'doctor/d_appoinment.html',d)
def update_status(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.get(id=pid)
    form=AppointmentForm(request.POST or None,instance=data)
    if request.method=="POST":
        u=request.POST['a_date']
        v=request.POST['a_timing']
        data.a_date=u
        data.a_timing=v
        data.status="confirmed"
        data.save()
        return redirect("d_appointment")
    d={'form':form,'data':data}
    return render(request,'doctor/update_status.html',d)
def confirmed_p_appointment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'patient/confirmed_p_appoinment.html',d)
def confirmed_d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    time_now=datetime.datetime.now()
    expiration_time=time_now+datetime.timedelta(seconds=36)
    round_off_time=round(expiration_time.timestamp())
    headers= {"alg":"HS256","typ":"JWT"}
    template =render_to_string('doctor/email_template.html',{'name':request.user.first_name})
    email="healthicde@gmail.com"
    url="https://api.zoom.us/v2/users/{}/meetings".format(email)
    date=datetime.datetime(2022,7,5,13,30).strftime("%Y-%m-%d T%H:%M:%S")
    obj={"topic":"Test Booking","starttime":date,"duration":30,"password":"12345"}
    mheader={"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjVRbVZWX2c4Um1xSmgySElOY0w4VEEiLCJleHAiOjE2Mzg2ODM3MDUsImlhdCI6MTYzODA3ODkwNn0.DLJ5wLRHtZwf_5vfeSxXc7S6xbg_BI1MoNj1Y3y7b70"}

    create_meeting=requests.post(url,json=obj,headers=mheader)
    final=create_meeting.text

    data_dict = json.loads(final)
    zoom_link= data_dict["start_url"]
    email = EmailMessage(
        'Appointment Confirmation',
        '' + template + '' + zoom_link ,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently=False
    email.send()
    return render(request,'doctor/confirmed_d_appoinment.html',d)
def history_p_appointment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'patient/history_p_appoinment.html',d)
def history_d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'doctor/history_d_appoinment.html',d)
def Login_Admin(request):
    error = False
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = True
    d = {'error': error}
    return render(request, 'login.html', d)
def admin_dashboard(request):
    t_doc = Doctor.objects.all().count()
    t_pat = Patient.objects.all().count()
    t_app2 = Appointment.objects.all().count()
    d = {'t_doc':t_doc,'t_pat':t_pat,'t_app2':t_app2}
    return render(request,'admin/admin_dashboard.html',d)
def admin_view_appointment(request):
    data=Appointment.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_appointment.html',d)
def admin_view_doctors(request):
    data=Doctor.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_doctors.html',d)
def admin_view_patients(request):
    data=Patient.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_patients.html',d)
def cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('p_appointment')
def doctor_cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('d_appointment')
def d_search_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        u=request.POST['from_date']
        v=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(u)
        i2 = datetime.datetime.fromisoformat(v)
        data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    d={'data':data,'u':u,'v':v}
    return render(request,'doctor/d_search_appoinment.html',d)
def doctor_status(request,pid):
    pat = Doctor.objects.get(id=pid)
    if pat.status=="pending":
        pat.status = "accept"
        pat.save()
        messages.success(request,'Selected Doctor granted to Permission')
    else:
        pat.status = "pending"
        pat.save()
        messages.success(request, 'Selected Doctor Withdraw to Permission')
    return redirect('admin_view_doctors')
def admin_profile(request):
    return render(request,'admin/profile.html')
def edit_admin_profile(request):
    data = Adminstration.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            f = request.POST['fname']
            l = request.POST['lname']
            m = request.POST['mobile']
            a = request.POST['address']
            e = request.POST['email']
            try:
                i = request.FILES['images']
                data.image = i
                data.save()
            except:
                pass
            data.user.first_name = f
            data.user.last_name = l
            data.user.email = e
            data.address = a
            data.mobile = m
            data.image = i
            data.user.save()
            data.save()
            messages.success(request,'Profile Updated Successfully')
        except:
            pass
        try:
            n = request.POST['pwd1']
            c = request.POST['pwd2']
            d = request.POST['pwd3']
            if c == d:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(d)
                u.save()
                messages.success(request, 'Password Changed Successfully')
        except:
            pass
    return redirect('admin_profile')
def my_patient(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed")
    d = {'data':data}
    return render(request,'doctor/my_patient.html',d)
def doc_patient_dashboard(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Patient.objects.get(id=pid)
    data2 = Doctor.objects.get(user=request.user)
    pat = Appointment.objects.filter(patient = data)
    pat2 = Appointment.objects.filter(patient = data,doctor=data2,a_date = datetime.date.today()).first()
    if not pat2:
        pat2 = 0
    else:
        pat2 = pat2.id
    d = {'data': pat,'pat':data,'pat2':pat2}
    return render(request,'doctor/doc_patient_dashboard.html',d)
def delete_patient(request,pid):
    data = Patient.objects.get(id=pid)
    data.delete()
    messages.success(request,'Patient deleted successfully')
    return redirect('admin_view_patients')
