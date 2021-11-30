from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from health.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('login', Login,name="login"),
    path('register', Registeration,name="register"),
    path('logout', Logout,name="logout"),
    path('cancel_appointment<int:pid>', cancel_appointment,name="cancel_appointment"),
#Admin Url
    path('admin_dashboard', admin_dashboard,name="admin_dashboard"),
    path('admin_view_appointment', admin_view_appointment,name="admin_view_appointment"),
    path('admin_view_doctors', admin_view_doctors,name="admin_view_doctors"),
    path('admin_view_patients', admin_view_patients,name="admin_view_patients"),
    path('delete_patient<int:pid>', delete_patient,name="delete_patient"),
    path('admin_profile', admin_profile, name="admin_profile"),
    path('edit_admin_profile', edit_admin_profile, name="edit_admin_profile"),
#Patient Url
    path('patient_dashboard', patient_dashboard,name="patient_dashboard"),
    path('patient_profile', Patient_Profile,name="patient_profile"),
    path('change_password', Change_Password,name="change_password"),
    path('search_doctor', search_doctor,name="search_doctor"),
    path('requestAppointment<int:pid>', requestAppointment,name="requestAppointment"),
    path('appointment<int:pid>', appointment,name="appointment"),
    path('p_appointment', p_appointment,name="p_appointment"),
    path('confirmed_p_appointment',confirmed_p_appointment,name="confirmed_p_appointment"),
    path('history_p_appointment',history_p_appointment,name="history_p_appointment"),
    path('all_doctor_appointment',all_doctor_appointment,name="all_doctor_appointment"),
#Doctor Url
    path('doctor_dashboard', doctor_dashboard,name="doctor_dashboard"),
    path('doctor_profile', Doctor_Profile,name="doctor_profile"),
    path('doctor_change_password', Doctor_Change_Password,name="doctor_change_password"),
    path('d_appointment', d_appointment,name="d_appointment"),
    path('update_status<int:pid>', update_status,name="update_status"),
    path('confirmed_d_appointment',confirmed_d_appointment,name="confirmed_d_appointment"),
    path('history_d_appointment',history_d_appointment,name="history_d_appointment"),
    path('doctor_cancel_appointment<int:pid>', doctor_cancel_appointment, name="doctor_cancel_appointment"),
    path('doc_patient_dashboard<int:pid>', doc_patient_dashboard, name="doc_patient_dashboard"),
    path('doctor_status<int:pid>', doctor_status, name="doctor_status"),
    path('d_search_appointment',d_search_appointment,name="d_search_appointment"),
    path('my_patient', my_patient, name="my_patient"),
]