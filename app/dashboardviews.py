from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import Staff, DrugCategory, Drug, Patient
from .forms import StaffForm, DrugCategoryForm, DrugForm, PatientTreatmentForm, DrugPrescriptionForm


@login_required(login_url='login')
def nurseDashboardPage(request):
    pageTitle = 'Dashboard'

    context = {'pageTitle':pageTitle}
    return render(request, 'dashboard/nurse-dashboard.html', context)

@login_required(login_url='login')
def pharmacistDashboardPage(request):
    pageTitle = 'Dashboard'

    context = {'pageTitle':pageTitle}
    return render(request, 'dashboard/pharmacist-dashboard.html', context)

@login_required(login_url='login')
def accountantDashboardPage(request):
    pageTitle = 'Dashboard'

    context = {'pageTitle':pageTitle}
    return render(request, 'dashboard/accountant-dashboard.html', context)