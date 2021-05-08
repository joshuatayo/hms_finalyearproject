from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Staff, DrugCategory, Drug, Patient, CardPayment, Appointment
from .forms import StaffForm, DrugCategoryForm, DrugForm, PatientTreatmentForm, DrugPrescriptionForm, CardPaymentForm, PatientForm


import datetime
import random
import string
import secrets

#dashboardPage
@login_required(login_url='login')
def dashboardPage(request):
    pageTitle = 'Dashboard'

    context = {'pageTitle':pageTitle}
    return render(request, 'receptionist/dashboard.html', context)

#patientPage
@login_required(login_url='login')
def patientPage(request):
    pageTitle = 'Patients'
    patients = Patient.objects.all()

    context = {
        'pageTitle':pageTitle,
        'patients':patients
    }
    return render(request, 'patient/all-patient.html', context)

#addPatientPage
@login_required(login_url='login')
def addPatientPage(request):
    pageTitle = 'Add Patients'
    cardPayments = CardPayment.objects.all()
    patientForm = PatientForm()

    if request.method == "POST":
        patientForm = PatientForm(request.POST)
        if patientForm.is_valid():
            if Patient.objects.filter(patient_id = request.POST['patient_id']).exists():
                messages.error(request, "Patient Already Exists")
                return redirect("receptionistaddpatient")
            else:
                current_user = request.user
                staff = Staff.objects.get(user = current_user)

                patient = Patient()
                patient.patient_id = request.POST['patient_id']
                patient.firstname = request.POST['firstname']
                patient.middlename = request.POST['middlename']
                patient.surname = request.POST['surname']
                patient.dob = request.POST['dob']
                patient.gender = request.POST['gender']
                patient.marital_status = request.POST['marital_status']
                patient.phone_number = request.POST['phone_number']
                patient.email = request.POST['email']
                patient.address = request.POST['address']
                patient.city_town = request.POST['city_town']
                patient.state = request.POST['state']
                patient.zipcode = request.POST['zipcode']
                patient.staff = Staff.objects.get(id = staff.id)
                patient.save()

                messages.success(request, "Patient Added Successfully")
                return redirect("receptionistaddpatient")

    context = {
        'pageTitle':pageTitle,
        'cardPayments':cardPayments,
        'patientForm':patientForm,
    }
    return render(request, 'patient/add-patient.html', context)


#appointmentPage
@login_required(login_url='login')
def appointmentPage(request):
    pageTitle = 'Appointment'
    appointments = Appointment.objects.all()

    if request.method == "POST":
        current_user = request.user
        staff = Staff.objects.get(user = current_user)
        cardNumber = request.POST['card_number']
        patient = Patient.objects.get(patient_id = cardNumber)

        appointment = Appointment()
        appointment.patient = Patient.objects.get(id = patient.id)
        appointment.status = request.POST['status']
        appointment.staff = Staff.objects.get(id = staff.id)
        appointment.save()

        messages.success(request, "Added Successfully")
        return redirect("receptionistappointmentpage")


    context = {
        'pageTitle':pageTitle,
        'appointments':appointments,
    }
    return render(request, 'patient/appointment.html', context)


