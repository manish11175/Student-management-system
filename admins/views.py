from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.urls import	reverse_lazy 
from django.views.generic.edit	import	CreateView,	UpdateView,DeleteView
from django.views.generic.list	import	ListView
from student.models import	Student,StuMedical,StuLocalGuard,Attendance,TotalAttendance
from student.models import  StuBank,StuHostel,StuBank,StuAdmission,Stu_placement
from django.contrib.auth.mixins	import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import redirect,	get_object_or_404 
from django.views.generic.base	import	TemplateResponseMixin,	View 

from django.forms.models import	modelform_factory 
from django.apps	import	apps 
from django.db.models import Count 
from student.models import StudentResult,StudentMidsem,StudentFee,StudentAddress,StudentResident
from student.models import Student,batch,Family
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators	import	login_required
from account.models import Profile
from django.contrib import messages
from student.forms import StudentSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.contrib.auth.models import User,auth
from hod.models import Class
import datetime
from.models import Footer,Carausal
def admin_autherization(user):
    try:
        return user.adminprofile.role=='admin'
    except ObjectDoesNotExist:
        pass


@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def admin_dash(request):
    return render(request,'admin/admin_dash.html')
@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def admin_profile(request):
    return render(request,'admin/admin_profile.html')



@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def college_hod(request):
    hod=Profile.objects.filter(designation='hod',activate=True)
    Hod=[]
    for h in hod:
        hods=User.objects.get(username=h.user)
        Hod.append(hods)
    return  render(request,'admin/college_hod.html',{'hod':Hod})


@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def StartNewBatch(request):
    now=datetime.datetime.now()
    user=request.user
    year=now.year
    
    if request.method=='POST':
        bat=request.POST['batch']
        bat=int(bat)
        batc=batch.objects.latest('batch')
        if batch.objects.filter(batch=bat).exists():
            messages.info(request,'Batch Already Exist')
            return redirect('start_new_batch')
            
        if bat<int(batc.batch):
            messages.warning(request,'This batch can not created')
            return redirect('start_new_batch')

        if batch.objects.filter(batch=bat).exists():
            messages.error(request,'Batch Already Exist')
            return redirect('start_new_batch')
            
    
        if bat<=year:
            y=batch.objects.create(batch=bat)
            y.save()
            for i in range(1,9):
                s=str(i)
                Class.objects.create(year=y,branch='cs',sem=s,sec='A')
                Class.objects.create(year=y,branch='cs',sem=s,sec='B')
                Class.objects.create(year=y,branch='it',sem=s,sec='A')
                Class.objects.create(year=y,branch='ce',sem=s,sec='A')
                Class.objects.create(year=y,branch='me',sem=s,sec='A')
                Class.objects.create(year=y,branch='ee',sem=s,sec='A')
                Class.objects.create(year=y,branch='ec',sem=s,sec='A')
                
            messages.success(request,'Batch Created Successfully')
            return render(request,"admin/start_batch.html")
        else:
            messages.info(request,'this year is coming soon.......')
            return redirect('start_new_batch')
    return render(request,"admin/start_batch.html")



@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def web_settings(request):
    return render(request,'website/website_menu.html')

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def footer_link(request):
    if request.method=='POST':
        link_cate=request.POST['link_cate']
        link_name=request.POST['link_name']
        link=request.POST['link']
        if Footer.objects.filter(link_cate=link_cate,link_name=link_name).exists():
            messages.error(request,'This link is already added ! ')
            return redirect('footer_link')
        else:
            f=Footer.objects.create(link_cate=link_cate,link_name=link_name,link=link)
            f.save()
            messages.success(request,'Added Successfully ')
            return redirect('footer_link')
    return render(request,'website/footer_link.html')

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def carausal(request):
    if request.method=='POST':
        slide_no=request.POST['slide_no']
        description=request.POST['description']
        title=request.POST['title']
        image=request.FILES['image']
        if Carausal.objects.filter(slide_no=slide_no).exists():
            c=Carausal.objects.filter(slide_no=slide_no)
            c.delete()
            c=Carausal.objects.create(slide_no=slide_no,title=title,description=description,image=image)
            c.save()
            messages.success(request,'updated successfully')
            return redirect('carausal')
        else:
            messages.error(request,'invalid attempt !')
            return redirect('carausal')
    else:
        carausal=Carausal.objects.all()
        return render(request,'website/carausal.html',{'carausal':carausal})