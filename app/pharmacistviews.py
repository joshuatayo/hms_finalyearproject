from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    return render(request, 'pharmacist/dashboard.html', context)

#drugPage
@login_required(login_url='login')
def drugPage(request):
    pageTitle = 'Drug'
    drugCategoryForm = DrugCategoryForm()
    drugInventoryForm = DrugInventoryForm()
    drugForm = DrugForm()
    drugs = Drug.objects.all()
    drugInventories = DrugInventory.objects.all()
    drugCategories = DrugCategory.objects.all()

    context = {
        'pageTitle':pageTitle,
        'drugCategoryForm':drugCategoryForm, 
        'drugInventoryForm':drugInventoryForm,
        'drugForm':drugForm, 
        'drugs':drugs,
        'drugCategories':drugCategories,
        'drugInventories':drugInventories
    }
    return render(request, 'pharmacist/drug.html', context)

@login_required(login_url='login')
def addDrugCategory(request):
    if request.method == "POST":
        drugCategoryForm = DrugCategoryForm(request.POST)
        if drugCategoryForm.is_valid(): 
            if DrugCategory.objects.filter(name = request.POST['name']).exists():
                messages.success(request, "Name already exists")
            else:
                drugCategory = DrugCategory()
                drugCategory.name = request.POST['name']
                drugCategory.save()
                messages.success(request, "Save Successfully")
    return redirect("pharmacistdrug")

# add drug
# @login_required(login_url='login')
# def addDrug(request):
#     if request.method == "POST":
#         drugInflowForm = DrugInflowForm(request.POST)
#         drugForm = DrugForm(request.POST)

#         if drugInflowForm.is_valid() and drugForm.is_valid():  
#             if Drug.objects.filter(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype']).exists():
#                 drug = Drug.objects.get(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype'])
#                 if DrugInflow.objects.filter(invoiceid = request.POST['invoiceid'], drug = drug.pk).exists():
#                     messages.success(request, "Already Exists")
#                     return redirect("pharmacistdrug")
#                 # drug.name = request.POST['name']
#                 # drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
#                 # drug.drugtype = request.POST['drugtype']
#                 drug.quantity = drug.quantity + int(request.POST['quantity'])
#                 # drug.price = request.POST['price']
#             else:
#                 drug = Drug()
#                 drug.name = request.POST['name']
#                 drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
#                 drug.drugtype = request.POST['drugtype']
#                 drug.quantity = request.POST['quantity']
#                 drug.price = request.POST['price']
            
#             drug.save()

#             drugInflow = DrugInflow()
#             drugInflow.invoiceid = request.POST['invoiceid']
#             drugInflow.drug = Drug.objects.get(id = drug.id)
#             drugInflow.quantity = request.POST['quantity']
#             current_user = request.user
#             staff = Staff.objects.get(user = current_user)
#             drugInflow.staff = Staff.objects.get(id = staff.id)
#             drugInflow.save()

#             messages.success(request, "Added Successfully")
        
#     return redirect("pharmacistdrug")

# @login_required(login_url='login')
# def editDrugCategory(request):
#     if request.method == "POST":
#         if DrugCategory.objects.filter(name = request.POST['name']).exists() and DrugCategory.objects.filter(pk == request.POST['id']):
#             messages.success(request, "Name already exists")
#         else:  
#             drugCategory = DrugCategoryFor.objects.get(pk=request.POST['id'])
#             drugCategory.name = request.POST['name']
#             drugCategory.save()
#             messages.success(request, "Updated Successfully")
#     return redirect("pharmacistdrug")
    

@login_required(login_url='login')
def patientdrugPage(request):
    pageTitle = 'Patient Drug'
    
    context = {
        'pageTitle':pageTitle,
    }
    return render(request, 'pharmacist/patientdrug.html', context)