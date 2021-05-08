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
    return render(request, 'doctor/dashboard.html', context)

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
        # appointment.status = request.POST['status']
        appointment.staff = Staff.objects.get(id = staff.id)
        appointment.save()

        messages.success(request, "Added Successfully")
        return redirect("receptionistappointmentpage")


    context = {
        'pageTitle':pageTitle,
        'appointments':appointments,
    }
    return render(request, 'patient/appointment.html', context)