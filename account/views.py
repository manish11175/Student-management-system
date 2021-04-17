
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from.forms import LoginForm,UserRegistrationForm,ProfileEditForm,UserEditForm,StudentProfileEditForm,AdminProfileEditForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators	import	login_required
from.models	import	Profile,StudentProfile,AdminProfile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.conf import settings
from student.models import Student,Tgcalling
from django.contrib.auth.models import User,auth
import json,requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test

def hod_autherization(user):
    try:
        return user.profile.designation=='hod'
    except ObjectDoesNotExist:
        pass
def admin_autherization(user):
    try:
        return user.adminprofile.role=='admin'
    except ObjectDoesNotExist:
        pass


def teacher_autherization(user):
    try:
        return user.profile.designation=='faculty'
    except ObjectDoesNotExist:
        pass
def user_autherization(user):
    try:
        return user.studentprofile.role=='student'
    except ObjectDoesNotExist:
        pass

def	teacher_login(request):
  
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if Profile.objects.filter(user=a).exists():
                b=Profile.objects.get(user=a.pk)
                if b.designation=='faculty' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('teacher_dash')
                    else:
                        messages.error(request,'Invalid Username or password')  
                        return redirect('/account/teacherlogin/')
                else:
                    messages.error(request,'Your Account is not Activated by Admin')  
                    return redirect('/account/teacherlogin/')
            else:
                messages.error(request,'Unauthrized Access')
                return redirect('/account/teacherlogin/')
        else:
            messages.error(request,'Your Account is not Created. Kindly Register Yourself')  
            return redirect('/account/teacherlogin/')
    return	render(request,	'registration/teacher_login.html')

def	hod_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if Profile.objects.filter(user=a).exists():
                b=Profile.objects.get(user=a.pk)
                if b.designation=='hod' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/hod/hoddash/')
                    else:
                        messages.error(request,'Invalid Username or password')  
                        return redirect('/account/hodlogin/')
                else:
                    messages.error(request,'Unauthrized Access')  
                    return redirect('/account/hodlogin/')
            else:
                messages.error(request,'Unauthrized Access')
                return redirect('/account/hodlogin/')
        else:
            messages.error(request,'You have not any  Account')  
            return redirect('/account/hodlogin/')
    return	render(request,	'account/hod_login.html')

def	admin_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if AdminProfile.objects.filter(user=a).exists():
                b=AdminProfile.objects.get(user=a.pk)
                if b.role=='admin' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/admins/admindash/')
                    else:
                        messages.error(request,'Invalid Username or password')  
                        return redirect('/account/adminlogin/')
                else:
                    messages.error(request,'Unauthrized Access')  
                    return redirect('/account/adminlogin/')
            else:
                messages.error(request,'Unauthrized Access')
                return redirect('/account/adminlogin/')
        else:
            messages.error(request,'You have not any  Account')  
            return redirect('/account/adminlogin/')
    return	render(request,	'account/admin_login.html')


        
        

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')    
def teacher_logout(request):
    auth.logout(request)
    return redirect('teacher_login')
@user_passes_test(admin_autherization,login_url='/account/adminlogin/')    
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')

def	student_login(request):
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if StudentProfile.objects.filter(user=a).exists():
                b=StudentProfile.objects.get(user=a.pk)
                if b.role=='student' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/user/studentdash/')
                    else:
                        messages.error(request,'Invalid Username or password')  
                        return redirect('/account/student_login/')
                else:
                    messages.error(request,'Your Account is not Activated by Tutour Guardian')  
                    return redirect('/account/student_login/')
            else:
                messages.error(request,'Unauthrized Access')
                return redirect('/account/student_login/')
        else:
            messages.error(request,'Your Account is not Created. Kindly Register Yourself')  
            return redirect('/account/student_login/')
 
    return render(request,'account/student_login.html')

@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def student_logout(request):
    auth.logout(request)
    return redirect('student_login')

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')  
def hod_logout(request):
    auth.logout(request)
    return redirect('hod_login')


def	register(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        photo=request.FILES['photo']
        designation=request.POST['designation']
        department=request.POST['department']
        if designation=='hod':
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request,"username already exists")
                    return redirect('/account/register/')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,"email already taken")
                    return redirect('/account/register/')
                else:
                    new_user=User.objects.create_superuser(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                    new_user.save()
                    Profile.objects.create(user=new_user,department=department,designation=designation,photo=photo)	
                    return	render(request,'account/register_done.html',{'new_user':	new_user})
            else:
                messages.error(request,"password didn't match ")
                return redirect('/account/register/')
        elif designation=='faculty':
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request,"username already exists")
                    return redirect('/account/register/')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,"email already taken")
                    return redirect('/account/register/')
                else:
                    new_user=User.objects.create_superuser(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                    new_user.save()
                    Profile.objects.create(user=new_user,department=department,designation=designation,photo=photo,activate=False)	
                    return	render(request,'account/register_done.html',{'new_user':new_user})
            else:
                messages.error(request,"password didn't match ")
                return redirect('/account/register/')
        else:
            return	render(request,	'account/register.html')
    return	render(request,	'account/register.html')

def	StudentRegister(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        photo=request.FILES['photo']
        role=request.POST['role']
        department=request.POST['department']
        batch=request.POST['batch']
        sec=request.POST['sec']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,"username already exists")
                return redirect('/account/studentregister/')
            elif User.objects.filter(email=email).exists():
                messages.error(request,"email already taken")
                return redirect('/account/studentregister/')

            else:
                new_user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                
                new_user.save()
                StudentProfile.objects.create(user=new_user,department=department,role=role,batch=batch,photo=photo,sec=sec)	
                


                return	render(request,'account/register_done.html',{'new_user':	new_user})
        else:
            messages.error(request,"password didn't match ")
            return redirect('/account/studentregister/')
    else:
        return	render(request,	'account/studentregister.html')
    								
        			
    return	render(request,	'account/studentregister.html')

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def	adminedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=AdminProfileEditForm(instance=request.user.adminprofile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('admin_profile')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('admin_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=AdminProfileEditForm(instance=request.user.adminprofile)				
    return	render(request,'account/adminedit.html',{'user_form':user_form,'profile_form':profile_form})



@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def	hodedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return	redirect('hod_profile')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'account/hod_edit.html',{'user_form':user_form,'profile_form':profile_form})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def	edit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return redirect('teacher_profile')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/edit.html',{'user_form':user_form,'profile_form':profile_form})

@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def	student_edit(request):
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=StudentProfileEditForm(instance=request.user.studentprofile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return	redirect('student_profile')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=StudentProfileEditForm(instance=request.user.studentprofile)				
    return	render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})
				
@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def StudentPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password was successfully updated!')
            return render(request,'user/student_profile.html')
        else:
            messages.error(request,'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/change_password.html', {'form': form})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return	render(request,'account/dashboard.html')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/password_change.html', {'form': form})


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def HodPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('hod_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/hod_pass_change.html', {'form': form})

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def AdminPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/admin_pass_change.html', {'form': form})




        