from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Staff, DrugCategory, Drug, Patient, CardPayment
from .forms import StaffForm, DrugCategoryForm, DrugForm, PatientTreatmentForm, DrugPrescriptionForm, CardPaymentForm


import datetime
import random
import string
import secrets


login_required(login_url='login')
def cardPaymentPage(request):
    pageTitle = 'Card Payment'
    cardPaymentForm = CardPaymentForm()
    cardPayments = CardPayment.objects.all().order_by('-created_at')

    if request.method == "POST":
        cardPaymentForm = CardPaymentForm(request.POST)
        if cardPaymentForm.is_valid(): 
            now = datetime.datetime.now()
            cardId = str(now.year) + str(random.randint(100, 999))
            current_user = request.user
            staff = Staff.objects.get(user = current_user)
            
            cardPayment = CardPayment()
            cardPayment.name = request.POST['name']
            cardPayment.card_id = int(cardId)
            cardPayment.amount = request.POST['amount']
            cardPayment.staff = Staff.objects.get(id = staff.id)
            cardPayment.save()

            messages.success(request, "Added Successfully")
        
        return redirect("cardpayment")

    context = {
        'pageTitle':pageTitle,
        'cardPaymentForm':cardPaymentForm,
        'cardPayments':cardPayments,
    }
    return render(request, 'payment/cardpayment.html', context)




