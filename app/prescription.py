from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Drug, DrugCategory, DrugInventory, DrugPrescription, DrugPrescriptionStaff, Staff
from .forms import StaffForm, DrugCategoryForm, DrugForm, DrugInventoryForm, PatientTreatmentForm, DrugPrescriptionForm
from cart.cart import Cart

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


@login_required(login_url='login')
def editDrugCategory(request):
    if request.method == "POST":
        if DrugCategory.objects.filter(name=request.POST['name']).exists():
            messages.success(request, "Category Name already exist")
        else:
            drugCategory = DrugCategory.objects.get(pk=request.POST['id'])
            drugCategory.name = request.POST['name']
            drugCategory.save()
            messages.success(request, "Updated Successfully")
    return redirect("pharmacistdrug")

@login_required(login_url='login')
def deleteDrugCategory(request, id):
    drugCategory = DrugCategory.objects.get(pk=id)
    drugCategory.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("pharmacistdrug")


@login_required(login_url='login')
def addDrug(request):
    if request.method == "POST":
        drugInventoryForm = DrugInventoryForm(request.POST)
        drugForm = DrugForm(request.POST)

        if drugInventoryForm.is_valid() and drugForm.is_valid():  
            if Drug.objects.filter(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype']).exists():
                drug = Drug.objects.get(name = request.POST['name'], drugcategory = request.POST['drugcategory'], drugtype = request.POST['drugtype'])
                if DrugInventory.objects.filter(invoiceid = request.POST['invoiceid'], drug = drug.pk).exists():
                    messages.success(request, "Already Exists")
                    return redirect("pharmacistdrug")
                # drug.name = request.POST['name']
                # drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
                # drug.drugtype = request.POST['drugtype']
                drug.quantity = drug.quantity + int(request.POST['quantity'])
                # drug.price = request.POST['price']
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

            messages.success(request, "Added Successfully")
        
    return redirect("pharmacistdrug")


@login_required(login_url='login')
def editDrug(request):
    if request.method == "POST":
        if Drug.objects.filter(name=request.POST['name'], drugcategory=request.POST['drugcategory'], drugtype=request.POST['drugtype']).exists():
            messages.success(request, "Drug already exist")
        else:
            drug = Drug.objects.get(pk=request.POST['id'])
            drug.name = request.POST['name']
            drug.drugcategory = DrugCategory.objects.get(id = request.POST['drugcategory'])
            drug.drugtype = request.POST['drugtype']
            drug.save()
            messages.success(request, "Updated Successfully")
    return redirect("pharmacistdrug")

@login_required(login_url='login')
def deleteDrug(request, id):
    drug = Drug.objects.get(pk=id)
    drug.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("pharmacistdrug")



@login_required(login_url='login')
def ajax_load_drug(request):
    drugType = request.GET['drugtype']
    drugs = Drug.objects.filter(drugtype=drugType)
    return render(request, 'pharmacist/ajax-load-drug.html', {"drugs":drugs})

@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        drugId = request.POST['drug']
        quantity = int(request.POST['quantity'])
        drug = Drug.objects.get(id=drugId)
        if not quantity:
            quantity = 1

        cart = Cart(request)
        cart.add(drug,quantity)

        carts = cart.list()
        total_price = cart.get_total_price() 
        print(carts)
    context = {
        'carts':carts,
        'total_price':total_price
    }
    
    return render(request, 'pharmacist/drug-cart.html', context)

@login_required(login_url='login')
def delete_from_cart(request,id):
    cart = Cart(request)
    cart.remove(id)

    carts = cart.list()
    
    context = {
        'carts':carts,
    }
    return render(request, 'pharmacist/drug-cart.html', context)

@login_required(login_url='login')
def delete_from_cart(request,id):
    cart = Cart(request)
    cart.remove(id)

    carts = cart.list()
    
    context = {
        'carts':carts,
    }
    return render(request, 'pharmacist/drug-cart.html', context)

@login_required(login_url='login')
def updateTreatmentDrug(request):
    if request.method == 'POST':
        current_user = request.user
        staff = Staff.objects.get(user = current_user)
        drugPrescriptionIds = request.POST.getlist('id[]')
        for d in drugPrescriptionIds:
            drugPrescription = DrugPrescription.objects.get(pk=int(d))
            drugPrescription.status = 'Checked'
            drugPrescription.save()
        
            drugPrescriptionStaff = DrugPrescriptionStaff()
            drugPrescriptionStaff.drugprescription = DrugPrescription.objects.get(id = drugPrescription.id)
            drugPrescriptionStaff.staff = Staff.objects.get(id = staff.id)
            drugPrescriptionStaff.save()
            

    
    return render(request, 'patient/edit-treatment.html',)

@login_required(login_url='login')
def deleteTreatmentDrug(request, id):
    drugPrescription = DrugPrescription.objects.get(pk=id)
    drugPrescription.delete()
    return redirect('patientpreviewcard', patient_id=drugPrescription.patienttreatment.patient.patient_id)
    

    

