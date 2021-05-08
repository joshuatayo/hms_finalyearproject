from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from .models import Staff, DrugCategory, Drug, CardPayment, Patient, Appointment, PatientTreatment, DrugPrescription, PatientTreatmentStaff, DrugPrescriptionStaff, TreatmentPayment
from .forms import StaffForm, DrugCategoryForm, DrugForm, PatientTreatmentForm, DrugPrescriptionForm, PatientForm, CardPaymentForm
from cart.cart import Cart


import datetime
import random
import string
import secrets


@login_required(login_url='login')
def allPatientPage(request):
    pageTitle = 'Patients'
    patients = Patient.objects.all().order_by('-created_at')

    context = {
        'pageTitle':pageTitle,
        'patients':patients
    }
    return render(request, 'patient/all-patient.html', context)

@login_required(login_url='login')
def addPatientPage(request):
    pageTitle = 'Add Patients'
    cardPayments = CardPayment.objects.filter(patient__isnull=True)
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

                cardPayment = CardPayment.objects.get(card_id=request.POST['patient_id'])
                cardPayment.patient = Patient.objects.get(id = patient.id)
                cardPayment.save()

                messages.success(request, "Patient Added Successfully")
                return redirect("addpatientpage")

    context = {
        'pageTitle':pageTitle,
        'cardPayments':cardPayments,
        'patientForm':patientForm,
    }
    return render(request, 'patient/add-patient.html', context)

@login_required(login_url='login')
def bookAppointment(request):
    pageTitle = 'Appointment'
    appointments = Appointment.objects.all()

    if request.method == "POST":
        current_user = request.user
        staff = Staff.objects.get(user = current_user)
        cardNumber = request.POST['card_number']
        patient = Patient.objects.get(patient_id = cardNumber)

        appointment = Appointment()
        appointment.patient = Patient.objects.get(id = patient.id)
        appointment.status = 'Queue'
        appointment.staff = Staff.objects.get(id = staff.id)
        appointment.save()

        messages.success(request, "Appointment Book Successfully")
        return redirect("allpatientpage")

    context = {
        'pageTitle':pageTitle,
        'appointments':appointments,
    }
    return render(request, 'patient/appointment.html', context)


@login_required(login_url='login')
def previewCardPage(request, patient_id=0):
    pageTitle = 'Patient Card'
    currentdate = datetime.datetime.now()
    patient = Patient.objects.get(patient_id=patient_id)
    patientTreatments = PatientTreatment.objects.all().filter(patient=patient.id).order_by('-created_at')
    #patientTreatment = PatientTreatment.objects.get(patient=patient.id)
    # drugPrescriptions = DrugPrescription.objects.all().filter(patienttreatment=patientTreatment.id)
    drugs = Drug.objects.all()

    context = {
        'pageTitle':pageTitle, 
        'currentdate':currentdate,
        'patient':patient,
        'patientTreatments':patientTreatments,
        # 'drugPrescriptions':drugPrescriptions,
    }
    return render(request, 'patient/patient-card.html', context)

@login_required(login_url='login')
def submitTreatment(request):
    if request.method == "POST":
        current_user = request.user
        staff = Staff.objects.get(user = current_user)
        cardNumber = request.POST['card_number']
        patient = Patient.objects.get(patient_id = cardNumber)
        cart = Cart(request)
        carts = cart.list()
        drugTotalAmount = sum(c['price'] for c in carts)
        
        patientTreatment = PatientTreatment()
        patientTreatment.treatment_id = "T" + str(random.randint(10000, 99999))
        patientTreatment.complaint = request.POST['complaint']
        patientTreatment.diagnosis = request.POST['diagnosis']
        patientTreatment.recommend = request.POST['recommend']
        patientTreatment.amount = request.POST['amount']
        patientTreatment.status = request.POST['status']
        patientTreatment.total_amount = int(request.POST['amount']) + drugTotalAmount
        patientTreatment.patient = Patient.objects.get(id = patient.id)
        patientTreatment.save()

        
        if carts is not None:
            for c in carts:
                drugPrescription = DrugPrescription()
                drugPrescription.drug = Drug.objects.get(id = c['id'])
                drugPrescription.quantity = c['quantity']
                drugPrescription.price = c['price']
                drugPrescription.patienttreatment = PatientTreatment.objects.get(id = patientTreatment.id)
                drugPrescription.save()

        patientTreatmentStaff = PatientTreatmentStaff()
        patientTreatmentStaff.patienttreatment = PatientTreatment.objects.get(id = patientTreatment.id)
        patientTreatmentStaff.staff = Staff.objects.get(id = staff.id)
        patientTreatmentStaff.save()
    
    return redirect('patientpreviewcard', patient_id=cardNumber)


@login_required(login_url='login')
def editTreatment(request):
    if request.method == 'GET':
        id = request.GET['treatmentId']
        patientTreatment = PatientTreatment.objects.get(pk=id)
        drugPrescriptions = DrugPrescription.objects.all().filter(patienttreatment=patientTreatment.id)
    
    else:
        cart = Cart(request)
        carts = cart.list()
        drugTotalAmount = sum(c['price'] for c in carts)
        patientTreatment = PatientTreatment.objects.get(id=request.POST['treatment'])
        patientTreatment.complaint = request.POST['complaint']
        patientTreatment.diagnosis = request.POST['diagnosis']
        patientTreatment.recommend = request.POST['recommend']
        patientTreatment.status = request.POST['status']
        patientTreatment.amount = request.POST['amount']
        patientTreatment.save()

        if carts is not None:
            for c in carts:
                drugPrescription = DrugPrescription()
                drugPrescription.drug = Drug.objects.get(id = c['id'])
                drugPrescription.quantity = c['quantity']
                drugPrescription.price = c['price']
                drugPrescription.patienttreatment = PatientTreatment.objects.get(id = patientTreatment.id)
                drugPrescription.save()

        drugPrescriptions = DrugPrescription.objects.all().filter(patienttreatment=patientTreatment.id)
        drugTotalAmount = sum(d['price'] for d in drugPrescriptions.values())
        patientTreatment2 = PatientTreatment.objects.get(id = patientTreatment.id)
        patientTreatment2.total_amount = Decimal(Decimal(request.POST['amount']) + drugTotalAmount)
        patientTreatment2.save()


    context = {
        'patientTreatment':patientTreatment,
        'drugPrescriptions':drugPrescriptions,
    }
    return render(request, 'patient/edit-treatment.html', context)

@login_required(login_url='login')
def deleteTreatment(request, id):
    patientTreatment = PatientTreatment.objects.get(pk=id)
    patientTreatment.delete()
    messages.success(request, "Treatment has been deleted successfully")
    return redirect('patientpreviewcard', patient_id=patientTreatment.patient.patient_id)

@login_required(login_url='login')
def addPayment(request):
    if request.method == 'POST':
        current_user = request.user
        staff = Staff.objects.get(user = current_user)
        patientTreatment = PatientTreatment.objects.get(pk=request.POST['treatment_id'])
        treatmentPayments = TreatmentPayment.objects.all().filter(patienttreatment = request.POST['treatment_id'])
        totalPaid = sum(p['amount_paid'] for p in treatmentPayments.values())
        print('you')
        if patientTreatment.total_amount != totalPaid:
            if (totalPaid + int(request.POST['amount_paid'])) <= patientTreatment.total_amount:
                treatmentPayment = TreatmentPayment()
                treatmentPayment.invoice_id = "#" + "I" + str(random.randint(10000, 99999))
                treatmentPayment.patienttreatment = PatientTreatment.objects.get(id = request.POST['treatment_id'])
                treatmentPayment.method = request.POST['method']
                treatmentPayment.fullname = request.POST['fullname']
                treatmentPayment.mobile_no = request.POST['mobile_no']
                treatmentPayment.amount_paid = request.POST['amount_paid']
                treatmentPayment.staff = Staff.objects.get(id = staff.id)
                treatmentPayment.save()

                treatmentPayments2 = TreatmentPayment.objects.all().filter(patienttreatment = treatmentPayment.patienttreatment)
                totalPaid2 = sum(p['amount_paid'] for p in treatmentPayments2.values())

                totalPaid = patientTreatment.amount + totalPaid2
                patientTreatment.total_amount_paid = totalPaid
                patientTreatment.save()
            else:
                messages.success(request, "Amount Paid is more than treatment price")
        else:
            messages.success(request, "Treatment payment is already complete")

    return redirect('patientpreviewcard', patient_id=patientTreatment.patient.patient_id)

@login_required(login_url='login')
def showPayment(request):
    if request.method == 'GET':
        id = request.GET['treatmentId']
        patientTreatment = PatientTreatment.objects.get(pk=id)
        treatmentPayments = TreatmentPayment.objects.all().filter(patienttreatment=patientTreatment).order_by('-created_at')

    context = {
        'treatmentPayments':treatmentPayments,
    }
    return render(request, 'patient/show-payment.html', context)

@login_required(login_url='login')
def showPaymentInvoice(request):
    if request.method == 'GET':
        id = request.GET['paidId']
        treatmentPayment = TreatmentPayment.objects.get(pk=id)
        drugPrescriptions = DrugPrescription.objects.all().filter(patienttreatment=treatmentPayment.patienttreatment.id)
        totalAmount = sum(d['price'] for d in drugPrescriptions.values())

    context = {
        'treatmentPayment':treatmentPayment,
        'drugPrescriptions':drugPrescriptions,
        'totalAmount':totalAmount
    }
    return render(request, 'patient/payment-invoice.html', context)

@login_required(login_url='login')
def deletePayment(request):
    if request.method == 'GET':
        id = request.GET['paidId']
        treatmentPayment = TreatmentPayment.objects.get(pk=id)
        treatmentPayment.delete()
    
    return render(request, 'patient/show-payment.html')

@login_required(login_url='login')
def InPatientPage(request):
    pageTitle = 'In-Patient'
    patientTreatments = PatientTreatment.objects.all().filter(status="InPatient").order_by("-updated_at")

    context = {
        'pageTitle':pageTitle,
        'patientTreatments':patientTreatments
    }
    return render(request, 'patient/in-patient.html', context)

@login_required(login_url='login')
def OutPatientPage(request):
    pageTitle = 'Out-Patient'
    patientTreatments = PatientTreatment.objects.all().filter(status="OutPatient").order_by("-updated_at")

    context = {
        'pageTitle':pageTitle,
        'patientTreatments':patientTreatments
    }
    return render(request, 'patient/out-patient.html', context)