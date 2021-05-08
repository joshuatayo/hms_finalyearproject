from django.forms import  ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput, TextInput, Select, Textarea, EmailInput, NumberInput

from .models import Staff, DrugCategory, Drug, DrugInventory, PatientTreatment, DrugPrescription, CardPayment, Patient

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['firstname', 'middlename', 'surname', 'dob', 'gender', 'marital_status', 'phone_number', 'group', 'address', 'city_town', 'state', 'zipcode',]
        widgets = { 
            'firstname': TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'middlename': TextInput(attrs={'class':'form-control', 'placeholder':'Middle Name'}),
            'surname': TextInput(attrs={'class':'form-control', 'placeholder':'Surname'}),
            'dob': DateInput(attrs={'type':'date', 'class':'form-control', 'data-date-autoclose':'true', 'placeholder':'Date of Birth'}),
            'gender': Select(attrs={'class':'custom-select'}),
            'marital_status': Select(attrs={'class':'custom-select'}),
            'phone_number': TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'group': Select(attrs={'class':'custom-select'}),
            'address': Textarea(attrs={'class':'form-control', 'rows':'5', 'placeholder':'Address'}),
            'city_town': TextInput(attrs={'class':'form-control', 'placeholder':'City/Town'}),
            'state': TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
            'zipcode': TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
        }

#drug forms
class DrugCategoryForm(ModelForm):
    class Meta:
        model = DrugCategory
        fields = ['name',]
        widgets = { 
            'name': TextInput(attrs={'class':'form-control', 'placeholder':'Category Name'}),
        }

class DrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'drugcategory', 'drugtype', 'quantity', 'price',]
        widgets = { 
            'name': TextInput(attrs={'class':'form-control', 'placeholder':'Drug Name'}),
            'drugcategory': Select(attrs={'class':'custom-select'}),
            'drugtype': Select(attrs={'class':'custom-select'}),
            'quantity': NumberInput(attrs={'class':'form-control', 'min':'0',}),
            'price': NumberInput(attrs={'class':'form-control',}),
        }

class DrugInventoryForm(ModelForm):
    class Meta:
        model = DrugInventory
        fields = ['invoiceid']
        widgets = { 
            'invoiceid': TextInput(attrs={'class':'form-control', 'placeholder':'Invoice Id'}),
        }

# patient
class PatientTreatmentForm(ModelForm):
    class Meta:
        model = PatientTreatment
        fields = ['patient', 'complaint', 'diagnosis', 'recommend', 'status',]

class DrugPrescriptionForm(ModelForm):
    class Meta:
        model = DrugPrescription
        fields = ['drug', 'quantity', 'price',]

class CardPaymentForm(ModelForm):
    class Meta:
        model = CardPayment
        fields = ['name', 'amount',]
        widgets = { 
            'name': TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),
            # 'card_type': Select(attrs={'class':'custom-select'}),
            'amount': NumberInput(attrs={'class':'form-control',}),
        }

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['firstname', 'middlename', 'surname', 'dob', 'gender', 'marital_status', 'phone_number', 'email', 'address', 'city_town', 'state', 'zipcode',]
        widgets = { 
            'firstname': TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'middlename': TextInput(attrs={'class':'form-control', 'placeholder':'Middle Name'}),
            'surname': TextInput(attrs={'class':'form-control', 'placeholder':'Surname'}),
            'dob': DateInput(attrs={'type':'date', 'class':'form-control', 'data-date-autoclose':'true', 'placeholder':'Date of Birth'}),
            'gender': Select(attrs={'class':'custom-select'}),
            'marital_status': Select(attrs={'class':'custom-select'}),
            'phone_number': TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'email': EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'address': Textarea(attrs={'class':'form-control', 'rows':'5', 'placeholder':'Address'}),
            'city_town': TextInput(attrs={'class':'form-control', 'placeholder':'City/Town'}),
            'state': TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
            'zipcode': TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
        }

# class UserForm(UserCreationForm):
#     class  Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']