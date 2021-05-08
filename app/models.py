from django.db import models
from django.contrib.auth.models import Group, User
from django_mysql.models import JSONField
# Create your models here.

#staff 
class Staff(models.Model):
    GERDER = (
        ('', '- Gender -'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    MaritalStatus = (
        ('', '- Marital Status -'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )
    staff_id = models.IntegerField()
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=10, choices=GERDER)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus)
    # email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    city_town = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', default='avatar.png')
    group = models.ForeignKey(Group, verbose_name=("Group"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=("User"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname + ' ' + self.surname

#Drug 
class DrugCategory(models.Model): 
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Drug(models.Model):
    DRUGTYPE = (
            ('Capsules', 'Capsules'),
            ('Injection', 'Injection'),
            ('Liquid', 'Liquid'),
            ('Tablet', 'Tablet'),
        )
    name = models.CharField(max_length=255)
    drugcategory = models.ForeignKey(DrugCategory, verbose_name=("DrugCategory"), on_delete=models.CASCADE, blank=True, null=True)
    drugtype = models.CharField(max_length=255, choices=DRUGTYPE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DrugInventory(models.Model):
    invoiceid = models.CharField(max_length=255, blank=True, null=True)
    drug = models.ForeignKey(Drug, verbose_name=("Drug"), on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

#Patient
class Patient(models.Model):
    GERDER = (
        ('', '- Gender -'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    MaritalStatus = (
        ('', '- Marital Status -'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )
    patient_id = models.IntegerField()
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus,)
    gender = models.CharField(max_length=10, choices=GERDER)
    address = models.TextField(blank=True, null=True) 
    city_town = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname

# class PatientHistory(models.Model):
#     history = JSONField()
#     patient = models.ForeignKey(Patient, verbose_name=("Patient"), on_delete=models.CASCADE)

class PatientTreatment(models.Model):
    treatment_id = models.CharField(max_length=255, blank=True, null=True)
    patient = models.ForeignKey(Patient, verbose_name=("Patient"), on_delete=models.CASCADE)
    complaint = models.TextField(blank=True, null=True) 
    diagnosis = models.TextField(blank=True, null=True) 
    recommend = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    amount =  models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PatientTreatmentStaff(models.Model):
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    patienttreatment = models.ForeignKey(PatientTreatment, verbose_name=("PatientTreatment"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class DrugPrescription(models.Model):
    drug = models.ForeignKey(Drug, verbose_name=("Drug"), on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    patienttreatment = models.ForeignKey(PatientTreatment, verbose_name=("PatientTreatment"), on_delete=models.CASCADE)
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DrugPrescriptionStaff(models.Model):
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    drugprescription = models.ForeignKey(DrugPrescription, verbose_name=("DrugPrescription"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class CardPayment(models.Model):
    # CARDTYPE = (
    #     ('', '- Card Type -'),
    #     ('OPD', 'OPD'),
    #     ('InPatient', 'InPatient'),
    # )
    name = models.CharField(max_length=500,)
    # card_type = models.CharField(max_length=10, choices=CARDTYPE,)
    card_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,)
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, verbose_name=("Patient"), on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Payment(models.Model):
#     patientid = models.IntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2,)
#     staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class TreatmentPayment(models.Model):
    invoice_id = models.CharField(max_length=255, blank=True, null=True)
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    patienttreatment = models.ForeignKey(PatientTreatment, verbose_name=("PatientTreatment"), on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    mobile_no = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)
    patient = models.ForeignKey(Patient, verbose_name=("Patient"), on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, verbose_name=("Staff"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    

