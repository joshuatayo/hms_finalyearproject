#app/urls.py
from django.urls import path
from . import views, dashboardviews, adminviews, pharmacistviews, paymentviews, receptionistviews, doctorviews, patientviews, prescription, paymentviews

urlpatterns = [
    path('', views.loginPage, name="login"), #loginPage
    path('logout/', views.logoutUser, name="logout"), #logoutUser
    path('staff/profile/', views.staffProfilePage, name="staffprofile"), #staffprofilePage
    path('staff/profile/changepassword/', views.changePassword, name="changepassword"),
    # path('test/', views.test, name="test"), #test

    #dashboard
    path('nurse/dashboard/', dashboardviews.nurseDashboardPage, name="nursedashboard"),
    path('pharmacist/dashboard/', dashboardviews.pharmacistDashboardPage, name="pharmacistdashboard"),
    path('accountant/dashboard/', dashboardviews.accountantDashboardPage, name="accountantdashboard"),

    # administrator
    path('administrator/dashboard/', adminviews.dashboardPage, name="admindashboard"), #admindashboardPage
    path('administrator/staffs/', adminviews.allStaffPage, name="adminallstaff"), #adminallstaff
    path('administrator/staff/add/', adminviews.addStaffPage, name="adminaddstaff"), #adminaddstaff
    path('administrator/staff/view/<int:staff_id>/', adminviews.editStaffPage, name="admineditstaff"), #admineditstaff
    path('administrator/staff/changepassword/', adminviews.changeStaffPassword, name="adminchangestaffpassword"),
    path('administrator/drug/', adminviews.drugPage, name="admindrug"), #admindrugPage
    path('administrator/patient/', adminviews.patientPage, name="adminpatient"), #adminpatientPage
    path('administrator/card/<int:patient_id>/', adminviews.adminPatientCardPage, name="adminpatientcard"), #adminPatientCardPage

    # pharmacist
    path('pharmacist/drug/', pharmacistviews.drugPage, name="pharmacistdrug"), #pharmacistdrugPage 
    path('pharmacist/drug/category/add', pharmacistviews.addDrugCategory, name="pharmacistadddrugcategory"),
    # path('pharmacist/drug/add/', pharmacistviews.addDrug, name="pharmacistadddrug"),  
    path('pharmacist/patient/drug/', pharmacistviews.patientdrugPage, name="pharmacistpatientdrug"), #pharmacistpatientdrugPage 

   
    path('payment/cardpayment/', paymentviews.cardPaymentPage, name="cardpayment"), #accountantcardpaymentPage

    # receptionist
    path('receptionist/dashboard/', receptionistviews.dashboardPage, name="receptionistdashboard"), #receptionistdashboardPage
    path('receptionist/patient/', receptionistviews.patientPage, name="receptionistpatient"), #receptionistpatientPage
    path('receptionist/appointment/', receptionistviews.appointmentPage, name="receptionistappointmentpage"), #receptionistappointmentPage

    # doctor
    path('doctor/dashboard/', doctorviews.dashboardPage, name="doctordashboard"), #dashboardPage 
    path('doctor/appointment/', doctorviews.appointmentPage, name="doctorappointmentpage"), #doctorappointmentPage

    # patient
    path('patient/patients/', patientviews.allPatientPage, name="allpatientpage"),
    path('patient/patients/add', patientviews.addPatientPage, name="addpatientpage"),
    path('patient/appointment/book', patientviews.bookAppointment, name="bookappointment"),
    path('patient/card/<int:patient_id>/', patientviews.previewCardPage, name="patientpreviewcard"), 
    path('patient/treatment/submit/', patientviews.submitTreatment, name="submittreatment"), 
    path('patient/treatment/edit/', patientviews.editTreatment, name="edittreatment"),
    path('patient/treatment/delete/<int:id>/', patientviews.deleteTreatment, name="deletetreatment"), 
    path('patient/treatment/payment/add/', patientviews.addPayment, name="addpayment"), 
    path('patient/treatment/payment/showpayment/', patientviews.showPayment, name="showpayment"),
    path('patient/treatment/payment/deletepayment/', patientviews.deletePayment, name="deletepayment"),
    path('patient/treatment/payment/showpaymentinvoice/', patientviews.showPaymentInvoice, name="showpaymentinvoice"),

    path('treatment/inpatient', patientviews.InPatientPage, name="inpatientpage"),
    path('treatment/outpatient', patientviews.OutPatientPage, name="outpatientpage"),

    path('pharmacist/drug/category/add', prescription.addDrugCategory, name="adddrugcategory"),
    path('pharmacist/drug/category/update', prescription.editDrugCategory, name="editdrugcategory"),
    path('pharmacist/drug/category/delete/<int:id>/', prescription.deleteDrugCategory, name="deletedrugcategory"),
    path('pharmacist/drug/add', prescription.addDrug, name="adddrug"),
    path('pharmacist/drug/update', prescription.editDrug, name="editdrug"),
    path('pharmacist/drug/delete/<int:id>/', prescription.deleteDrug, name="deletedrug"),
    path('patient/load/drug/', prescription.ajax_load_drug, name="ajaxloaddrug"),
    path('addtocart/', prescription.add_to_cart, name="addtocart"),
    path('deletefromcart/<int:id>/', prescription.delete_from_cart, name="deletefromcart"),
    path('patient/treatment/drug/delete/<int:id>/', prescription.deleteTreatmentDrug, name="deletetreatmentdrug"),
    path('patient/treatment/drug/update', prescription.updateTreatmentDrug, name="updatereatmentdrug"),
    
    
]