from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Staff, User


# Create your views here.
#loginpage
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                current_user = request.user
                staff = Staff.objects.get(user = current_user)
                request.session['profile_image'] = staff.profile_image.url
                request.session['firstname'] = staff.firstname
                request.session['surname'] = staff.surname
                request.session['group'] = group
                if  group == 'Administrator':
                    return redirect('admindashboard')
                elif group == 'Doctor':
                    return redirect('doctordashboard')
                elif group == 'Nurse':
                    return redirect('nursedashboard')
                elif group == 'Pharmacist':
                    return redirect('pharmacistdashboard')
                elif group == 'Accountant':
                    return redirect('accountantdashboard')
                elif group == 'Receptionist':
                    return redirect('receptionistdashboard')
                else:
                    return HttpResponse('Not allow')
        else:
            messages.info(request, 'Username Or Password is incorrect')
    
    return render(request, 'loginpage.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def staffProfilePage(request):
    pageTitle = 'Profile'
    current_user = request.user
    staff = Staff.objects.get(user =current_user)

    if request.method == "POST":
        staffId = request.POST['id']
        staff = Staff.objects.get(pk=staffId)
        staff.middlename = request.POST['middlename']
        staff.dob = request.POST['dob']
        staff.gender = request.POST['gender']
        staff.marital_status = request.POST['marital_status']
        staff.phone_number = request.POST['phone_number']
        staff.email = request.POST['email']
        staff.address = request.POST['address']
        staff.city_town = request.POST['city_town']
        staff.state = request.POST['state']
        staff.zipcode = request.POST['zipcode']
        staff.save()

        isUser = request.POST.get('usercheck')
        if isUser == 'usercheck':
            userId = request.POST['user_id']
            user = User.objects.get(pk=userId)
            user.email = request.POST['email']
            user.save()

        messages.success(request, "Updated Successfully")
        return redirect('staffprofile')

    context = {
        'pageTitle':pageTitle,
        'staff':staff,
    }
    return render(request, 'layout/profile.html', context)


@login_required(login_url='login')
def changePassword(request):
    if request.method == "POST":
        if request.POST['new_password'] == request.POST['confirm_password']:
            userId = request.POST['id']
            user = User.objects.get(pk=userId)
            staffId = request.POST['staff_id']
            if user.set_password == request.POST['old_password']:
                newPassword = request.POST['new_password']
                user.set_password(newPassword)
                user.save()

                messages.success(request, "Password Change Successfully")
                return redirect("staffprofile") 
            else:
                messages.warning(request, "Old password is incorrect")
        else:
            messages.warning(request, "Password not the same")
    return redirect("staffprofile")