from django.contrib import admin
from app.models import Staff, DrugCategory, Drug, DrugInventory, Patient, CardPayment, Appointment, PatientTreatment, DrugPrescription

# Register your models here.
#staff
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'firstname', 'surname', 'user', 'group', 'gender', 'created_at', 'updated_at')
    ordering = ('staff_id', 'firstname', 'surname', 'created_at',)
    search_fields = ('staff_id', 'firstname', 'lastname',)

admin.site.register(Staff, StaffAdmin)

#drug
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(DrugCategory, DrugCategoryAdmin)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'drugcategory', 'drugtype', 'quantity', 'price', 'created_at', 'updated_at')
    ordering = ('name', 'drugcategory', 'drugtype',)
    search_fields = ('name', 'drugcategory',)

admin.site.register(Drug, DrugAdmin)

class DrugInventoryAdmin(admin.ModelAdmin):
    list_display = ('invoiceid', 'drug', 'quantity', 'staff', 'date')
    ordering = ('invoiceid', 'date',)
    search_fields = ('invoiceid', 'drug', 'staff', 'date',)

admin.site.register(DrugInventory, DrugInventoryAdmin)

#patient
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'firstname', 'surname', 'phone_number', 'gender', 'staff', 'created_at', 'updated_at')
    ordering = ('firstname', 'surname', 'created_at',)
    search_fields = ('firstname', 'lastname',)

admin.site.register(Patient, PatientAdmin)

#cardpayment
class CardPaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_id', 'amount', 'staff', 'created_at', 'updated_at')
    ordering = ('card_id', 'created_at',)
    search_fields = ('name', 'card_id', )

admin.site.register(CardPayment, CardPaymentAdmin)

#appointment
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'staff', 'status', 'created_at', 'updated_at')
    ordering = ('patient', 'staff', 'created_at',)
    search_fields = ('patient', 'status',)

admin.site.register(Appointment, AppointmentAdmin)

#patientTreatment
class PatientTreatmentAdmin(admin.ModelAdmin):
    list_display = ('patient',  'status', 'total_amount', 'created_at', 'updated_at')
    ordering = ('patient', 'status', 'created_at',)
    search_fields = ('patient', 'status',)

admin.site.register(PatientTreatment, PatientTreatmentAdmin)

#DrugPrescription
class DrugPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('drug',  'quantity', 'price', 'patienttreatment', 'created_at', 'updated_at')
    ordering = ('drug', 'quantity', 'created_at',)
    search_fields = ('drug', 'price',)

admin.site.register(DrugPrescription, DrugPrescriptionAdmin)