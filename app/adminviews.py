from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import Staff, DrugCategory, Drug, DrugInventory, Patient
from .forms import StaffForm, DrugCategoryForm, DrugForm, DrugInventoryForm, PatientTreatmentForm, DrugPrescriptionForm


import datetime
import random
import string
import secrets

#dashboardPage
@login_required(login_url='login')
def dashboardPage(request):
    pageTitle = 'Dashboard'

    context = {'pageTitle':pageTitle}
    return render(request, 'admin/dashboard.html', context)

#staffPage
@login_required(login_url='login')
def allStaffPage(request):
    pageTitle = 'All Staffs'
    staffs = Staff.objects.all()

    context = {
        'pageTitle':pageTitle, 
        'staffs':staffs,
    }
    return render(request, 'admin/all-staff.html', context)

@login_required(login_url='login')
def addStaffPage(request):
    pageTitle = 'Add Staff'
    # userForm = UserForm()
    staffForm = StaffForm()

    if request.method == 'POST':
        staffForm = StaffForm(request.POST)
        if staffForm.is_valid():
            if Staff.objects.filter(phone_number = request.POST['phone_number']).exists():
                messages.warning(request, "Staff Exist Already")
                return redirect('adminaddstaff')
            else:
                staff = Staff()
                now = datetime.datetime.now()
                staffId = str(now.year) + str(random.randint(10, 99))
                staff.staff_id =  int(staffId)
                staff.firstname = request.POST['firstname']
                staff.middlename = request.POST['middlename']
                staff.surname = request.POST['surname']
                staff.dob = request.POST['dob']
                staff.gender = request.POST['gender']
                staff.marital_status = request.POST['marital_status']
                staff.phone_number = request.POST['phone_number']
                staff.email = request.POST['email']
                staff.group = Group.objects.get(id = request.POST['group'])
                staff.address = request.POST['address']
                staff.city_town = request.POST['city_town']
                staff.state = request.POST['state']
                staff.zipcode = request.POST['zipcode']
                staff.save()

                isUser = request.POST.get('usercheck')
                if isUser == 'usercheck':
                    user = User()
                    firstname = request.POST['firstname']
                    surname = request.POST['surname']
                    uname = firstname[0] + surname[0] + str(random.randrange(10, 99)) + 'AMS'
                    user.username = uname
                    user.first_name = firstname
                    user.last_name = surname
                    user.email = request.POST['email']
                    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(8))
                    password1 = password
                    user.set_password(password1)
                    user.save()
                    group = Group.objects.get(id = request.POST['group'])
                    user.groups.add(group)
                   

                    staff = Staff.objects.get(id = staff.id)
                    staff.user = User.objects.get(id = user.id)
                    staff.save()
                    send_mail('AMS', 'Username: '+ uname+ ' and Password: '+password1, 'joshuatayomatthew@gamil.com', [request.POST['email'],])

                messages.success(request, "Staff Saved successfully")
                return redirect('adminaddstaff')

    context = {
        'pageTitle':pageTitle,
        'staffForm':staffForm,
    }
    return render(request, 'admin/add-staff.html', context)

@login_required(login_url='login')
def editStaffPage(request, staff_id=0):
    pageTitle = 'Staff Profile'
    staff = Staff.objects.get(staff_id=staff_id)
    groups = Group.objects.all()

    if request.method == "POST":
        staffId = request.POST['id']
        staff = Staff.objects.get(pk=staffId)
        staff.firstname = request.POST['firstname']
        staff.middlename = request.POST['middlename']
        staff.surname = request.POST['surname']
        staff.dob = request.POST['dob']
        staff.gender = request.POST['gender']
        staff.marital_status = request.POST['marital_status']
        staff.phone_number = request.POST['phone_number']
        staff.email = request.POST['email']
        staff.group = Group.objects.get(id = request.POST['group'])
        staff.address = request.POST['address']
        staff.city_town = request.POST['city_town']
        staff.state = request.POST['state']
        staff.zipcode = request.POST['zipcode']
        staff.save()

        isUser = request.POST.get('usercheck')
        if isUser == 'usercheck':
            userId = request.POST['user_id']
            user = User.objects.get(pk=userId)
            firstname = request.POST['firstname']
            surname = request.POST['surname']
            user.username = firstname[0] + surname[0] + str(random.randrange(10, 99)) + 'AMS'
            user.email = request.POST['email']
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(8))
            password1 = password
            user.set_password(password1)
            user.save()
            
            send_mail('AMS', 'Username: '+ uname+ ' and Password: '+password1, 'joshuatayomatthew@gamil.com', [request.POST['email'],])

        return redirect('adminallstaff')

    context = {
        'pageTitle':pageTitle, 
        'staff':staff,
        'groups':groups,
    }
    return render(request, 'admin/edit-staff.html', context)

@login_required(login_url='login')
def changeStaffPassword(request):
    if request.method == "POST":
        if request.POST['new_password'] == request.POST['confirm_password']:
            userId = request.POST['id']
            user = User.objects.get(pk=userId)
            oldPassword = request.POST['old_password']
            staffId = request.POST['staff_id']
            if user.password == oldPassword:
                newPassword = request.POST['new_password']
                user.set_password(newPassword)
                user.save()

                messages.success(request, "Password Change Successfully")
                return redirect("adminallstaff") 
            else:
                messages.warning(request, "Old password is incorrect")
        else:
            messages.warning(request, "Password not the same")
    return redirect("adminallstaff")

#drugPage
@login_required(login_url='login')
def drugPage(request):
    drugCategoryForm = DrugCategoryForm()
    drugInventoryForm = DrugInventoryForm()
    drugForm = DrugForm()
    drugs = Drug.objects.all()
    # drugInventories = DrugInventory.objects.all()
    drugCategories = DrugCategory.objects.all()

    if request.method == 'POST':
        drugInventoryForm = DrugInventoryForm(request.POST)
        drugForm = DrugForm(request.POST)

        if drugInventoryForm.is_valid() and drugForm.is_valid():   
            if Drug.objects.filter(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype']).exists():
                drug = Drug.objects.get(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype'])
                drug.name = request.POST['name']
                drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
                drug.drugtype = request.POST['drugtype']
                drug.quantity = drug.quantity + int(request.POST['quantity'])
                drug.price = request.POST['price']
            else:
                drug = Drug()
                drug.name = request.POST['name']
                drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
                drug.drugtype = request.POST['drugtype']
                drug.quantity = request.POST['quantity']
                drug.price = request.POST['price']
            
            drug.save()

            drugInventory = DrugInventory()
            drugInventory.invoiceid = request.POST['invoiceid']
            drugInventory.drug = Drug.objects.get(id = drug.id)
            drugInventory.quantity = request.POST['quantity']
            current_user = request.user
            staff = Staff.objects.get(user = current_user)
            drugInventory.staff = Staff.objects.get(id = staff.id)
            drugInventory.save()

            return redirect('admindashboard')

    context = {
        'drugCategoryForm':drugCategoryForm, 
        'drugInventoryForm':drugInventoryForm, 
        'drugForm':drugForm, 
        'drugs':drugs,
        'drugCategories':drugCategories,
        'drugInventories':drugInventories
    }
    return render(request, 'admin/drug.html', context)

#patientPage
@login_required(login_url='login')
def patientPage(request):
    patients = Patient.objects.all()

    context = {'patients':patients}
    return render(request, 'admin/patient.html', context)

@login_required(login_url='login')
def adminPatientCardPage(request, patient_id=0):
    patient = Patient.objects.get(patient_id=patient_id)
    patientTreatmentForm = PatientTreatmentForm()
    drugPrescriptionForm = DrugPrescriptionForm()

    context = {
        'patient':patient,
        'patientTreatmentForm':patientTreatmentForm,
        'drugPrescriptionForm':drugPrescriptionForm,
    }
    return render(request, 'admin/card.html', context)

# def add_prescription_list(request.id):
#     if request.method == 'POST':
#         drug = Drug.objects.get(id=id)
        
#         prescription = Prescription(request)
        # prescription.add(drug,quantity)

