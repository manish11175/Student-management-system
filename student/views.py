from django.shortcuts import render
import math

import pandas as pd
from django.db.models import Q
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.utils import timezone
from django import forms
from account.models import StudentProfile
from django.urls import	reverse_lazy 
from django_countries.widgets import CountrySelectWidget
from django.views.generic.edit	import	CreateView,	UpdateView,DeleteView
from django.views.generic.list	import	ListView
from.models import	Student,StuMedical,Family,StudentAddress,Stu_placement,Tgcalling,StudentResident,StuAdmission
from.models import  StuBank,StuHostel,StudentFee,StudentMidsem,StudentResult,StudentEducation,StuLocalGuard,AttendanceMessages
from django.contrib.auth.mixins	import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import redirect,	get_object_or_404 
from django.views.generic.base	import	TemplateResponseMixin,	View 
from datetime import timedelta,date  
from django.forms.models import	modelform_factory 
from django.apps	import	apps 
from django.db.models import Count 
from .models import Student,batch,StudentFee,Attendance,TotalAttendance
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from .forms import StudentSearchForm
from search_views.search import SearchListView,ListView
from search_views.filters import BaseFilter
from django.core.exceptions import ObjectDoesNotExist
from hod.models import AssignCT,Class,Subject_sem,TeacherSubjectAttendance,TeacherSubjectMark,TeacherSubjectMidTerm,TeacherPracticalMark,TeacherProjectMark\
    ,TutorGuard
 
import django_excel as excel
from pyexcel_xlsx import *
from.resources import StudentResouce
from tablib import Dataset
import json
from django.conf import settings          
from twilio.rest import Client
from admins.models import Footer,Carausal
def teacher_autherization(user):
    try:
        return user.profile.designation=='faculty'
    except ObjectDoesNotExist:
        pass


def home(request):
    carausal=Carausal.objects.all()
    return render(request,'home/home.html',{'carausal':carausal})

def about(request):
    return render(request,'home/about.html')
def contact_us(request):
    return render(request,'home/contact.html')
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')   
def teacher_dash(request):
    return	render(request,	'dashboard.html')
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')   
def teacher_profile(request):
    return	render(request,	'teacher_profile.html')


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def tg_class(request):
    user=request.user
    return render(request,'students/class/tg_class.html')
    



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def add_student_excel(request):
    owner=request.user.pk
    if request.method=='POST':
        student_resource=StudentResouce()
        dataset=Dataset()
        new_student = request.FILES['excel']
        if not new_student.name.endswith('xlsx'):
            messages.error(request,"wrong format")
            return redirect('add_student_excel')
        imported_data=dataset.load(new_student.read(),format='xlsx')
        invalid_data=[]
        already=[]
        added=[]
       
        if len(imported_data)<0:
            messages.warning(request,'excel sheet is empty')
            return redirect('add_student_excel')
        for data in imported_data:
            
            if data!=None:
                try:
                    if Student.objects.filter(enrollment=data[0].lower()).exists():
                        already.append(data[0])
                    else:
                        if data[0]!=None:
                            value=Student(owner,data[0].lower(),data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12])
                            value.save()
                            added.append(data[0])
                        else:
                            invalid_data.append(data[0])

                except:
                    invalid_data.append(data[0])
            else:
                
                return render(request,'students/manage/student/add_student_excel.html',{'added':added,'already':already,'invalid':invalid_data})
        return render(request,'students/manage/student/add_student_excel.html',{'added':added,'already':already,'invalid':invalid_data})
    return render(request,'students/manage/student/add_student_excel.html')






class TestMixin1(UserPassesTestMixin,AccessMixin):
    login_url ='/account/teacherlogin/'
    def test_func(self):
        try:
            return self.request.user.profile.designation=='faculty'
        except ObjectDoesNotExist:
            pass

class StudentsFilter(BaseFilter):
    search_fields = {
        'search_text' : ['first_name', 'last_name','enrollment','Email'],
    }




class OwnerMixin(object):				
    def	get_queryset(self):
        qs=super(OwnerMixin,self).get_queryset()
        qs=qs.order_by('enrollment')								
        return	qs.filter(owner=self.request.user)

class OwnerEditMixin(object):				
    def	form_valid(self,form):								
        form.instance.owner	=self.request.user
        return super(OwnerEditMixin,self).form_valid(form)

class OwnerStudentMixin(OwnerMixin,	LoginRequiredMixin):				
    model=Student
    fields=['enrollment','first_name','last_name','Email','phone','photo','dob','gender','batch','branch','sem','sec']					
    success_url=reverse_lazy('manage_student_list')
class OwnerStudentEditMixin(OwnerStudentMixin,OwnerEditMixin):
    fields=['enrollment','first_name','last_name','Email','phone','photo','dob','gender','batch','branch','sem','sec']
    widgets={ 'enrollment':forms.TextInput(attrs={'class':'form-control'}),
            'dob':forms.DateInput(attrs={'class':'input','placeholder':'yyyy-mm-dd'})}		
    success_url=reverse_lazy('manage_student_list')				
    template_name='students/manage/student/form.html'



class ManageStudentListView(TestMixin1,OwnerStudentMixin,SearchListView):
    model = Student
  
    template_name = 'students/manage/student/list.html'
    form_class = StudentSearchForm
    filter_class = StudentsFilter

class StudentCreateView(TestMixin1,PermissionRequiredMixin,OwnerStudentEditMixin,CreateView):
    permission_required	='student.add_student'
   
class StudentUpdateView(TestMixin1,PermissionRequiredMixin,OwnerStudentEditMixin,UpdateView):
    permission_required	='student.change_student'				
    
class StudentDeleteView(TestMixin1,PermissionRequiredMixin,OwnerStudentMixin,DeleteView):
    
    template_name='students/manage/student/delete.html'				
    success_url	=reverse_lazy('manage_student_list')
    permission_required	='student.delete_student'
# creating filter in student





    
class StudentCreateView(PermissionRequiredMixin,OwnerStudentEditMixin,CreateView):
    permission_required	='student.add_student'
   
class StudentUpdateView(PermissionRequiredMixin,OwnerStudentEditMixin,UpdateView):
    permission_required	='student.change_student'				
    
class StudentDeleteView(PermissionRequiredMixin,OwnerStudentMixin,DeleteView):
    
    template_name='students/manage/student/delete.html'				
    success_url	=reverse_lazy('manage_student_clist')
    permission_required	='student.delete_student'


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_subject(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    dept=request.user.profile.department
    bat=student.batch.batch
    bat=int(bat)
    if request.method=='POST':
        sem=request.POST['sem']
        if sem<=student.sem:
            x=int(sem)//2
            bat+=x
            
            bats=batch.objects.get(batch=bat)
            if Subject_sem.objects.filter(year=bats,sem=sem,dept=dept).exists():
                subject=Subject_sem.objects.filter(year=bats,sem=sem,dept=dept)
                
                return render(request,'students/subject/student_subject.html',{'subject':subject,'student':student})
            else:
                messages.error(request,"subjects  not found")
                return redirect('teacher_student_subject',pk=pk)
        else:
            messages.error(request,"Subject not found in  {} semester ".format(sem))
            return redirect('teacher_student_subject',pk=pk)

    return render(request,'students/subject/student_subject.html',{'student':student})

    
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_unit_mark(request,pk,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='tutorial')
        mark1=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='test')
        return render(request,'students/subject/student_unit_mark_view.html',{'mark':mark,'mark1':mark1,'subject_id':subject_id,'student':student})
    else:
        messages.error(request,'Unit marks nor found !')
        return redirect('teacher_student_subject',pk=pk)

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_midterm_mark(request,pk,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'students/subject/student_midterm_view.html',{'mark':mark,'student':student,'subject':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('teacher_student_subject',pk=pk)
        

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_practical_mark(request,pk,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'students/subject/student_practical_mark_view.html',{'mark':mark,'student':student,'subject':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('teacher_student_subject',pk=pk)
        


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_project_mark(request,pk,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'students/subject/student_project_mark_view.html',{'mark':mark,'student':student,'subject_id':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('teacher_student_subject',pk=pk)
        






@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_subject_attendance(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    dept=request.user.profile.department
    bat=student.batch.batch
    bat=int(bat)
    if request.method=='POST':
        sem=request.POST['sem']
        if sem<=student.sem:
            x=int(sem)//2
            bat+=x
            bats=batch.objects.get(batch=bat)
            if Subject_sem.objects.filter(year=bats,sem=sem,dept=dept).exists():
                subject=Subject_sem.objects.filter(year=bats,sem=sem,dept=dept)
                object_list=[]
                for sub in subject:
                    att_class = TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=sub,attend=1).count()
                    total_class =TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=sub).count()
                    attendance=0
                    if total_class!=0:
                        attendance = round(att_class / total_class * 100, 2)
            
                    cta = math.ceil((0.75*total_class - att_class)/0.25)
                    if cta < 0:
                        cta=0
                    data=[sub,att_class,total_class,attendance,cta]
                    object_list.append(data)
                return render(request,'students/manage/attendance/subject_attendance.html',{'student':student,'object_list':object_list})
            else:
                messages.error(request,"you don't have attendance record")
                return render(request,'students/manage/attendance/subject_attendance.html',{'student':student})    
        else:
            messages.error(request,"Please Select the valid semester")
            return render(request,'students/manage/attendance/subject_attendance.html',{'student':student})
    return render(request,'students/manage/attendance/subject_attendance.html',{'student':student})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_sem_attendance(request,pk):
    labels = []
    data = []
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        sem=request.POST['sem']
        if Attendance.objects.filter(enrollment=student,sem=sem).exists():
            attend=Attendance.objects.filter(enrollment=student,sem=sem)
            att_class=Attendance.objects.filter(enrollment=student,sem=sem,attend=1).count()
            total_class=Attendance.objects.filter(enrollment=student,sem=sem).count()
            attendance = 0
            if total_class >0:
                attendance = round(att_class / total_class * 100, 2)
            cta = math.ceil((0.75*total_class - att_class)/0.25)
            if cta < 0:
                cta=0
            return render(request,'students/manage/attendance/student_attendance.html',{'attend':attend,'att_class':att_class,'total_class':total_class,'attendance':attendance,'cta':cta, 'labels': labels,'data': data,'student':student})
        else:
            messages.error(request,"attendance not found !")
            return render(request,'students/manage/attendance/student_attendance.html',{'student':student})
            
            
    else:
        return render(request,'students/manage/attendance/student_attendance.html',{'student':student})



#Adding details about the student resident
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_resident_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        house_no=request.POST['house_no']
        street=request.POST['street']
        city=request.POST['city']
        district=request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        if StudentResident.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('student_resident_update',pk=student.enrollment)
        else:
            s=StudentResident.objects.create(enrollment=student,house_no=house_no,street=street,city=city,district=district,\
                state=state,country=country,pincode=pincode)
            s.save()
            resident=StudentResident.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_resident.html',{'resident':resident,'student':student})
    else:
        if StudentResident.objects.filter(enrollment=student).exists():
            resident=StudentResident.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_resident.html',{'resident':resident,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_resident.html',{'student':student})
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_resident_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        house_no=request.POST['house_no']
        street=request.POST['street']
        city=request.POST['city']
        district=request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        if StudentResident.objects.filter(enrollment=student).exists():
            s=StudentResident.objects.filter(enrollment=student).update(house_no=house_no,street=street,city=city,district=district,\
                state=state,country=country,pincode=pincode)
          
            resident=StudentResident.objects.get(enrollment=student)
            messages.success(request,'address update successfully')
            
            return render(request,'students/manage/student/teacher_student_resident.html',{'resident':resident,'student':student})
        else:
            messages.error(request,'address not found !')
            return redirect('student_resident_update',pk=student.enrollment)
    return render(request,'students/manage/student/student_resident_edit.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_address_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        house_no=request.POST['house_no']
        street=request.POST['street']
        city=request.POST['city']
        district=request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        if StudentAddress.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('student_address_update',pk=student.enrollment)
        else:
            s=StudentAddress.objects.create(enrollment=student,house_no=house_no,street=street,city=city,district=district,\
                state=state,country=country,pincode=pincode)
            s.save()
            address=StudentAddress.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_address.html',{'address':address,'student':student})
    else:
        if StudentAddress.objects.filter(enrollment=student).exists():
            address=StudentAddress.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_address.html',{'address':address,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_address.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_address_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        house_no=request.POST['house_no']
        street=request.POST['street']
        city=request.POST['city']
        district=request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        if StudentAddress.objects.filter(enrollment=student).exists():
            s=StudentAddress.objects.filter(enrollment=student).update(house_no=house_no,street=street,city=city,district=district,\
                state=state,country=country,pincode=pincode)
          
            address=StudentAddress.objects.get(enrollment=student)
            messages.success(request,'address update successfully')
            return render(request,'students/manage/student/teacher_student_address.html',{'address':address,'student':student})
        else:
            messages.error(request,'address not found !')
            return redirect('student_address_update',pk=student.enrollment)
    return render(request,'students/manage/student/student_address_edit.html',{'student':student})


#Addinng Student Result
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_result_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        sem=request.POST['sem']
        result=request.POST['result']
        sgpa=request.POST['sgpa']
        sgpa=float(sgpa)
        cgpa=request.POST['cgpa']
        cgpa=float(cgpa)
        if_fail=request.POST['if_fail']
        marksheet=request.FILES['marksheet']
        if sgpa<=10 and cgpa<=10:
            if StudentResult.objects.filter(enrollment=student,sem=sem).exists():
                messages.error(request,'Result already added !')
                return redirect('student_result_update',pk=student.enrollment)
            else:
                result=StudentResult.objects.create(enrollment=student,sem=sem,result=result,sgpa=sgpa,cgpa=cgpa,if_fail=if_fail,marksheet=marksheet)
                result.save()
                object_list=StudentResult.objects.filter(enrollment=student)
                messages.success(request,'Result Recorded Successfully')	
                return render(request,'students/manage/student/student_result.html',{'object_list':object_list,'student':student})

        else:
            messages.error(request,'CGPA and SGPA must be less than 10')
            return redirect('student_result_update',pk=student.enrollment)
    else:
        if StudentResult.objects.filter(enrollment=student).exists():
            object_list=StudentResult.objects.filter(enrollment=student)
            return render(request,'students/manage/student/student_result.html',{'object_list':object_list,'student':student})
        else:
            return render(request,'students/manage/student/student_result.html',{'student':student})
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_result_edit(request,pk,sem):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        result=request.POST['result']
        sgpa=request.POST['sgpa']
        sgpa=float(sgpa)
        cgpa=request.POST['cgpa']
        cgpa=float(cgpa)
        if_fail=request.POST['if_fail']
        marksheet=request.FILES['marksheet']
        if sgpa<=10 and cgpa<=10:
            if StudentResult.objects.filter(enrollment=student,sem=sem).exists():
                result=StudentResult.objects.filter(enrollment=student,sem=sem).update(result=result,sgpa=sgpa,cgpa=cgpa,if_fail=if_fail,marksheet=marksheet)
               
                object_list=StudentResult.objects.filter(enrollment=student)
                messages.success(request,'Result update Successfully')	
                return render(request,'students/manage/student/student_result.html',{'object_list':object_list,'student':student})
            else:
                messages.error(request,'Result not found!')
                return redirect('student_result_update',pk=student.enrollment)
        else:
            messages.error(request,'CGPA and SGPA must be less than 10')
            return redirect('student_result_edit',pk=student.enrollment,sem=sem)
    return render(request,'students/manage/student/student_result_edit.html',{'student':student,'sem':sem})

#Addinng Student Mid sem result
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_midsem_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        sem=request.POST['sem']
        midterm=request.POST['midterm']
        total_mark=request.POST['total_mark']
        obtain_mark=request.POST['obtain_mark']
        obtain_mark=float(obtain_mark)
        total_mark=float(total_mark)
        avg=obtain_mark/(total_mark/100)
        if obtain_mark<=total_mark:
            if StudentMidsem.objects.filter(enrollment=student,sem=sem,midterm=midterm).exists():
                messages.error(request,'Already Marked !')
                return redirect('student_midsem_update',pk=student.enrollment)
            else:
                result=StudentMidsem.objects.create(enrollment=student,sem=sem,midterm=midterm,total_mark=total_mark,obtain_mark=obtain_mark,avg=avg)
                result.save()
                messages.success(request,'Result Recorded Successfully')	
                return redirect('student_midsem_update',pk=student.enrollment)
        else:
            messages.error(request,'obtain mark must equal or less then total mark')
            return redirect('student_midsem_update',pk=student.enrollment)
    else:
        if  StudentMidsem.objects.filter(enrollment=student).exists():
            object_list=StudentMidsem.objects.filter(enrollment=student)
            return render(request,'students/manage/student/student_midsem.html',{'object_list':object_list,'student':student})
        else:
            return render(request,'students/manage/student/student_midsem.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_midsem_edit(request,pk,sem,midterm):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        total_mark=request.POST['total_mark']
        obtain_mark=request.POST['obtain_mark']
        obtain_mark=float(obtain_mark)
        total_mark=float(total_mark)
        avg=obtain_mark/(total_mark/100)
        if obtain_mark<=total_mark:

            if StudentMidsem.objects.filter(enrollment=student,sem=sem,midterm=midterm).exists():
                result=StudentMidsem.objects.filter(enrollment=student,sem=sem,midterm=midterm).update(total_mark=total_mark,obtain_mark=obtain_mark,avg=avg)
                messages.success(request,'Result Update Successfully')	
                object_list=StudentMidsem.objects.filter(enrollment=student)
                return render(request,'students/manage/student/student_midsem.html',{'object_list':object_list,'student':student})
            else:
                messages.error(request,'Result not found !')	
                return redirect('student_midsem_update',pk=student.enrollment)

        else:
            messages.error(request,'obtain mark must equal or less then total mark')
            return redirect('student_midsem_edit',pk=student.enrollment,sem=sem,midterm=midterm)
    return render(request,'students/manage/student/student_midsem_edit.html',{'student':student,'sem':sem,'midterm':midterm})

#Addinng Student Fee
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_fee_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk,owner=request.user)
    if request.method=='POST':
        sem=request.POST['sem']
        total_amt=request.POST['total_amt']
        total_amt=float(total_amt)
        amt_due=request.POST['amt_due']
        amt_due=float(amt_due)
        amt_paid=request.POST['amt_paid']
        amt_paid=float(amt_paid)
        receipt_no=request.POST['receipt_no']
        date=request.POST['date']
        if StudentFee.objects.filter(enrollment=student,receipt_no=receipt_no).exists():
            messages.error(request,'Fees with this receipt no already added')
            return redirect('student_fee_update',pk=student.enrollment)
        else:
            fee=StudentFee.objects.create(enrollment=student,sem=sem,total_amt=total_amt,amt_due=amt_due,amt_paid=amt_paid,receipt_no=receipt_no,date=date)
            fee.save()
            messages.success(request,'Fee Recorded Successfully')	
            return redirect('student_fee_update',pk=student.enrollment)
    else:
        if StudentFee.objects.filter(enrollment=student).exists():
            fee=StudentFee.objects.filter(enrollment=student)
            return render(request,'students/manage/student/student_fee.html',{'object_list':fee,'student':student})
        else:
            return render(request,'students/manage/student/student_fee.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_fee_edit(request,pk,receipt):
    student=get_object_or_404(Student,enrollment=pk,owner=request.user)
    if request.method=='POST':
        sem=request.POST['sem']
        total_amt=request.POST['total_amt']
        total_amt=float(total_amt)
        amt_due=request.POST['amt_due']
        amt_due=float(amt_due)
        amt_paid=request.POST['amt_paid']
        amt_paid=float(amt_paid)
        receipt_no=request.POST['receipt_no']
        date=request.POST['date']
        if StudentFee.objects.filter(enrollment=student,receipt_no=receipt).exists():
            fee=StudentFee.objects.filter(enrollment=student,receipt_no=receipt).update(sem=sem,total_amt=total_amt,amt_due=amt_due,amt_paid=amt_paid,receipt_no=receipt_no,date=date)
           
            messages.success(request,'Fee update Successfully')
            fee=StudentFee.objects.filter(enrollment=student)
            return render(request,'students/manage/student/student_fee.html',{'object_list':fee,'student':student})
        else:
            messages.error(request,'Fees with this receipt no Not Found !')
            return redirect('student_fee_update',pk=student.enrollment)
    else:
        if StudentFee.objects.filter(enrollment=student,receipt_no=receipt).exists():
            fee=StudentFee.objects.get(enrollment=student,receipt_no=receipt)
            return render(request,'students/manage/student/student_fee_edit.html',{'fee':fee,'student':student})
        else:
            return render(request,'students/manage/student/student_fee_edit.html',{'student':student})

        

# student Stu_placement
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_placement_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        tnp_date=request.POST['tnp_date']
        placement_date=request.POST['placement_date']
        company_name=request.POST['company_name']
        placement_result=request.POST['placement_result']
        join_date=request.POST['join_date']
        placement_package=request.POST['placement_package']
        placement_remark=request.POST['placement_remark']
        placement=Stu_placement.objects.create(enrollment=student,tnp_date=tnp_date,placement_date=placement_date,company_name=company_name,\
                      placement_result=placement_result,join_date=join_date,placement_package=placement_package,placement_remark=placement_remark)
        placement.save()
        messages.success(request,'Placement  Recorded Successfully')
        return redirect('student_placement_update',pk=student.enrollment)
    else:
        if Stu_placement.objects.filter(enrollment=student).exists():
            placed=Stu_placement.objects.filter(enrollment=student)
            return render(request,'students/manage/student/student_placement.html',{'object_list':placed,'student':student})
        else:
            return render(request,'students/manage/student/student_placement.html',{'student':student})
					
       							
          
    
#Adding details about the student addmission
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_admission(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        entrance=request.POST['entrance']
        admisbase=request.POST['admisbase']
        sch_no=request.POST['sch_no']
        branch=request.POST['branch']
        sem=request.POST['sem']
        sec=request.POST['sec']
        year=request.POST['year']
        if StuAdmission.objects.filter(enrollment=student).exists():
            messages.error(request,"already added !")
            return redirect('student_admission',pk=student.enrollment)
            
        else:
            a=StuAdmission.objects.create(enrollment=student,entrance=entrance,admisbase=admisbase,sch_no=sch_no\
                ,branch=branch,sem=sem,sec=sec,year=year)
            a.save()
            messages.success(request,'added successfully')
            return redirect('student_admission',pk=student.enrollment)
    else:
        if StuAdmission.objects.filter(enrollment=student).exists():
            admission=StuAdmission.objects.get(enrollment=student)
            return render(request,'students/manage/student/student_admission.html',{'admission':admission,'student':student})
        else:
            return render(request,'students/manage/student/student_admission.html',{'student':student})

# student hostel details
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_hostel_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        name_hostel=request.POST['name_hostel']
        room_no=request.POST['room_no']
        resi_address=request.POST['resi_address']
        pincode=request.POST['pincode']
        if StuHostel.objects.filter(enrollment=student).exists():
            messages.error(request,"Already added !")
            return redirect('student_hostel_update',pk=student.enrollment)
        else:
            a=StuHostel.objects.create(enrollment=student,name_hostel=name_hostel,room_no=room_no,\
                resi_address=resi_address,pincode=pincode)
            a.save()
            messages.success(request,'added successfully')
            return redirect('student_hostel_update',pk=student.enrollment)
    else:
        if StuHostel.objects.filter(enrollment=student).exists():
            hostel=StuHostel.objects.get(enrollment=student)
            return render(request,'students/manage/student/student_hostel.html',{'hostel':hostel,'student':student})
        else:
            return render(request,'students/manage/student/student_hostel.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_hostel_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        name_hostel=request.POST['name_hostel']
        room_no=request.POST['room_no']
        resi_address=request.POST['resi_address']
        pincode=request.POST['pincode']
        StuHostel.objects.filter(enrollment=student).update(name_hostel=name_hostel,room_no=room_no,\
            resi_address=resi_address,pincode=pincode)
        hostel=StuHostel.objects.get(enrollment=student)
        messages.success(request,'added successfully')
        return render(request,'students/manage/student/student_hostel.html',{'hostel':hostel,'student':student})
    return render(request,'students/manage/student/student_hostel_edit.html',{'student':student})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_education(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        course=request.POST['course']
        roll_no=request.POST['roll_no']
        rank=request.POST['rank']
        board=request.POST['board']
        year_of_passing=request.POST['year_of_passing']
        total_mark=request.POST['total_mark']
        obtain_mark=request.POST['obtain_mark']
        percent=request.POST['percent']
        marksheet=request.FILES['marksheet']
        obtain_mark=float(obtain_mark)
        total_mark=float(total_mark)
        avg=obtain_mark/(total_mark/100)
        if obtain_mark<total_mark:
            if StudentEducation.objects.filter(enrollment=student,course=course).exists():
                messages.error(request,'details already exists !')
                return redirect('teacher_student_education',pk=student.enrollment)
                
            else:
                result=StudentEducation.objects.create(enrollment=student,course=course,roll_no=roll_no,rank=rank,board=board,year_of_passing=year_of_passing,total_mark=total_mark,obtain_mark=obtain_mark,percent=percent)
                result.save()
                object_list=StudentEducation.objects.filter(enrollment=student)
                messages.success(request,'Response Recorded Successfully')
                return render(request,'students/manage/student/teacher_student_education.html',{'object_list':object_list,'student':student})
                
        else:
            messages.error(request,'obtain mark should be less than total mark')
            return redirect('teacher_student_education',pk=student.enrollment)
    else:
        if  StudentEducation.objects.filter(enrollment=student).exists():
            object_list=StudentEducation.objects.filter(enrollment=student)
            return render(request,'students/manage/student/teacher_student_education.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'students/manage/student/teacher_student_education.html',{'student':student})




#Adding details about the student local guardian

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_lg_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        lg_name=request.POST['lg_name']
        lg_mob=request.POST['lg_mob']
        lg_address=request.POST['lg_address']
        stu_lg=request.POST['stu_lg']
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('student_lg_update',pk=student.enrollment)
        else:
            s=StuLocalGuard.objects.create(enrollment=student,local_guard_name=lg_name,guard_mob=lg_mob,\
                guard_address=lg_address,stu_rela_guard=stu_lg)
            s.save()
            lg=StuLocalGuard.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_lg.html',{'lg':lg,'student':student})
    else:
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            lg=StuLocalGuard.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_lg.html',{'lg':lg,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_lg.html',{'student':student})



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_lg_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        lg_name=request.POST['lg_name']
        lg_mob=request.POST['lg_mob']
        lg_address=request.POST['lg_address']
        stu_lg=request.POST['stu_lg']
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            s=StuLocalGuard.objects.filter(enrollment=student).update(local_guard_name=lg_name,guard_mob=lg_mob,\
                guard_address=lg_address,stu_rela_guard=stu_lg)
            lg=StuLocalGuard.objects.get(enrollment=student)
            messages.success(request,'lg update successfully')
            return render(request,'students/manage/student/teacher_student_lg.html',{'lg':lg,'student':student})
            
        else:
            messages.error(request,'Details not Found !')
            return redirect('student_lg_update',pk=student.enrollment)
            
    return render(request,'students/manage/student/teacher_student_lg_edit.html',{'student':student})
# student medical details

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_medical_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        blood_group=request.POST['blood_group']
        physical=request.POST['physical']
        other=request.POST['other']
        if StuMedical.objects.filter(enrollment=student).exists():
            messages.error(request,'Already added')
            return redirect('student_medical_update',pk=student.enrollment)
        else:
            s=StuMedical.objects.create(enrollment=student,blood_group=blood_group,physical_disable=physical,other_med=other)
            s.save()
            medical=StuMedical.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_medical.html',{'medical':medical,'student':student})
    else:
        if StuMedical.objects.filter(enrollment=student).exists():
            medical=StuMedical.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_medical.html',{'medical':medical,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_medical.html',{'student':student})

# student bank details

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_bank_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        bank_name=request.POST['bank_name']
        bank_branch=request.POST['bank_branch']
        bank_ac=request.POST['bank_ac']
        bank_ifsc=request.POST['bank_ifsc']
        ac_hold_name=request.POST['ac_hold_name']
        aadhar_no=request.POST['aadhar_no']
        if StuBank.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('student_bank_update',pk=student.enrollment)
        else:
            s=StuBank.objects.create(enrollment=student,bank_name=bank_name,bank_branch=bank_branch,bank_ac=bank_ac,bank_ifsc=bank_ifsc,\
                ac_hold_name=ac_hold_name,aadhar_no=aadhar_no)
            s.save()
            bank=StuBank.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_bank.html',{'bank':bank,'student':student})
    else:
        if StuBank.objects.filter(enrollment=student).exists():
            bank=StuBank.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_bank.html',{'bank':bank,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_bank.html',{'student':student})

# test

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_dash(request,pk):
    student=get_object_or_404(Student,enrollment=pk,owner=request.user)
    return render(request,'students/manage/student/teacher_student_dash.html',{'student':student})

#Adding details about the student family

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_family_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        father_name=request.POST['father_name']
        father_mob=request.POST['father_mob']
        father_email=request.POST['father_email']
        father_organi=request.POST['father_organi']
        father_occup=request.POST['father_occup']
        father_income=request.POST['father_income']
        father_office=request.POST['father_office']
        mother_name=request.POST['mother_name']
        mother_mob=request.POST['mother_mob']
        mother_email=request.POST['mother_email']
        mother_organi=request.POST['mother_organi']
        mother_occup=request.POST['mother_occup']
        mother_income=request.POST['mother_income']
        mother_office=request.POST['mother_office']
        if Family.objects.filter(enrollment=student).exists():
            messages.error(request,'family already exists')
            return redirect('student_family_update',pk=student.enrollment)
        else:
            f=Family.objects.create(enrollment=student,father_name=father_name,father_mob=father_mob,father_email=father_email,father_organi=father_organi,\
                father_occup=father_occup,father_income=father_income,father_office=father_office,mother_name=mother_name,mother_mob=mother_mob,mother_email=mother_email,\
                    mother_organi=mother_organi,mother_occup=mother_occup,mother_income=mother_income,mother_office=mother_office)
            f.save()
            family=Family.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'students/manage/student/teacher_student_family.html',{'family':family,'student':student})
            
    else:
        if Family.objects.filter(enrollment=student).exists():
            family=Family.objects.get(enrollment=student)
            return render(request,'students/manage/student/teacher_student_family.html',{'family':family,'student':student})
        else:
            return render(request,'students/manage/student/teacher_student_family.html',{'student':student})



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_list_view(request,pk):
    if Student.objects.filter(owner=request.user,enrollment=pk).exists():
        student=get_object_or_404(Student,enrollment=pk,owner=request.user)
        family=[]
        address=[]
        resident=[]
        if Family.objects.filter(enrollment=student).exists():
            f=Family.objects.get(enrollment=student)
            family.append(f)
        if StudentAddress.objects.filter(enrollment=student).exists():
            add=StudentAddress.objects.get(enrollment=student)
            address.append(add)
        if StudentResident.objects.filter(enrollment=student).exists():
            res=StudentResident.objects.get(enrollment=student)
            resident.append(res)
        return render(request,'students/manage/student/student_list.html',{'student':student,'family':family,'resident':resident,'address':address})
        
    else:
        messages.error(request,'Student not found !')
        return redirect('teacher_student_list',pk=request.user)

#under testing
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def t_attendance(request,pk):

    if request.method=='POST':
        user=request.user
        branch=request.user.profile.department
        bats=request.POST['batch']
        sem=request.POST['sem']
        sec=request.POST['sec']
        if Student.objects.filter(owner=user,batch=bats,branch=branch,sem=sem,sec=sec).exists():
            student=Student.objects.filter(owner=user,batch=bats,branch=branch,sem=sem,sec=sec) 
            return render(request,'students/manage/attendance/selected_student.html',{'student':student})
        else:
            messages.error(request,'Students not found!')
            return redirect('select_student',pk=pk)
    
    else:
        user=request.user
        dept=request.user.profile.department
        bat=batch.objects.latest('batch')
        Tg_Class=[]
        for b in range(int(bat.batch)-4,int(bat.batch)+1):
            if TutorGuard.objects.filter(branch=dept,year=b,teacher_id=user).exists():
                class_id=TutorGuard.objects.filter(branch=dept,year=b,teacher_id=user)
                for c in class_id:
                    Tg_Class.append(c)
        if Tg_Class is not None:
            return render(request,'students/manage/attendance/select.html',{'tg_class':Tg_Class})
        else:
            message.error(request,'You do not have any Tg class')
            return redirect('select_student',pk=pk)           
    
    
           
    

import datetime
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def studentattendance(request):
    if request.method=='POST':
        user=request.user
        branch=request.user.profile.department
        
        sem=request.POST['sem']
        batch=request.POST['batch']
        sec=request.POST['sec']
        date=request.POST['date']
        dates=date.split('-')
        y=int(dates[0])
        m=int(dates[1])
        d=int(dates[2])
        a_date = datetime.date(y,m,d)
        week_number = a_date.isocalendar()[1]
        if Student.objects.filter(owner=user,batch=batch,branch=branch,sem=sem,sec=sec).exists():
            student=Student.objects.filter(owner=user,batch=batch,branch=branch,sem=sem,sec=sec)
            for s in student:
                status=request.POST[s.enrollment]
                if Attendance.objects.filter(enrollment=s,date=date).exists():
                    messages.error(request,'Attendane on given date is  already submitted ')
                    return render(request,'students/manage/attendance/selected_student.html',{'student':student})
                else:
                    attendance=Attendance.objects.create(enrollment=s,sem=sem,date=date,attend=status,week=week_number)
                    attendance.save()
            messages.success(request,'attendance marked sucessfully')
            return redirect('select_student',pk=request.user.pk)
        else:
            return redirect('select_student',pk=request.user.pk)

    return redirect('select_student',pk=request.user.pk)


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def attendance_view(request,pk):
    if request.method=='POST':
        branch=request.user.profile.department
        batch=request.POST['batch']
        sem=request.POST['sem']
        sec=request.POST['sec']
        attend_list=[]
        if Student.objects.filter(owner=request.user,batch=batch,branch=branch,sem=sem,sec=sec).exists():
            student=Student.objects.filter(owner=request.user,batch=batch,branch=branch,sem=sem,sec=sec)
            for s in student:
                if Attendance.objects.filter(enrollment=s,sem=s.sem).exists():
                    att_class=Attendance.objects.filter(enrollment=s,sem=sem,attend=1).count()
                    total_class=Attendance.objects.filter(enrollment=s,sem=sem).count()
                    attendance = 0
                    if total_class >0:
                        attendance = round(att_class / total_class * 100, 2)
                    cta = math.ceil((0.75*total_class - att_class)/0.25)
                    if cta < 0:
                        cta=0
                    data=[s,att_class,total_class,attendance,cta]
                    attend_list.append(data)
            return render(request,'students/manage/attendance/attendance_view.html',{'attend_list':attend_list,'batch':batch,'sec':sec,'sem':sem})
        else:
            messages.error(request,'Student not found !')
            return redirect('select_student',pk=request.user.pk)   
    else:
        return render(request,'students/manage/attendance/attendance_view.html')



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def attendance_details(request,pk):
    
    student=get_object_or_404(Student,owner=request.user,enrollment=pk)
    if request.method=='POST':
        sem=request.POST['sem']
        if student.sem==sem:
            if Attendance.objects.filter(enrollment=student,sem=sem).exists():
                attend=Attendance.objects.filter(enrollment=student,sem=sem)
                return render(request,'students/manage/attendance/attendance_details.html',{'attend':attend})
        else:
            if Attendance.objects.filter(enrollment=student,sem=sem).exists():
                attend=Attendance.objects.filter(enrollment=student,sem=sem)
                return render(request,'students/manage/attendance/old_attendance_details.html',{'attend':attend})
            else:
                messages.error(request,'Attendance not found !')
                return redirect('attendance_view',pk=request.user.pk)
    else:
        
        return redirect('attendance_view',pk=request.user.pk)


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def attendance_update(request,pk,date):
    student=get_object_or_404(Student,owner=request.user,enrollment=pk)       
    attend=get_object_or_404(Attendance,enrollment=student,date=date)
    if request.method=='POST':
        status=request.POST[student.enrollment]
        if Attendance.objects.filter(enrollment=student.enrollment,date=date).exists():
            attendance=Attendance.objects.filter(enrollment=student.enrollment,date=date).update(attend=status)
           
            if Attendance.objects.filter(enrollment=student,sem=student.sem).exists():
                attend=Attendance.objects.filter(enrollment=student,sem=student.sem)
                messages.success(request,'Attendance Updated Sucessfully')
                return render(request,'students/manage/attendance/attendance_details.html',{'attend':attend})
           
        else:
            messages.error(request,'Attendance not found !')
            return redirect('attendance_details',pk=student.enrollment)

    return render(request,'students/manage/attendance/attendance_update.html',{'date':date,'student':student})
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def tgcalling(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    
    if request.method=='POST':
        date=request.POST['date']
        contact_no=request.POST['contact_no']
        contact_person=request.POST['contact_person']
        reason=request.POST['reason']
        description=request.POST['description']
        if Tgcalling.objects.filter(enrollment=student,date=date).exists():
            messages.error(request,'Call recorded already exists on given date')
            return redirect('tgcalling',student.enrollment)
        else:
            tgcall=Tgcalling.objects.create(enrollment=student,sem=student.sem,date=date,contact_no=contact_no,contact_person=contact_person,reason=reason,description=description,faculty=request.user)
            tgcall.save()
            object_list=Tgcalling.objects.filter(enrollment=student)
            messages.success(request,'Tgcall  Recorded Successfully')
            return render(request,'students/manage/student/tgcalling.html',{'student':student,'object_list':object_list})
       
   
    else:
        if Tgcalling.objects.filter(enrollment=student).exists():
            object_list=Tgcalling.objects.filter(enrollment=student)
            return render(request,'students/manage/student/tgcalling.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'students/manage/student/tgcalling.html',{'student':student})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def student_account_activate(request):
    student=StudentProfile.objects.filter(department=request.user.profile.department,role='student',activate=False)
    Students=[]
    if request.method=='POST':
        for s in student:
            stu=User.objects.get(username=s.user)
            Students.append(stu)
            active=request.POST[stu.username]
            ac=StudentProfile.objects.filter(user=stu).update(activate=active)
            
        messages.success(request,"Student account activated  successfully")    
        return redirect('teacher_dash')
    return  render(request,'students/manage/student/student_account_request.html',{'student':student})
 
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')			
def student_attendance_view(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if Attendance.objects.filter(enrollment=student,sem=student.sem).exists():
        attend=Attendance.objects.filter(enrollment=student,sem=student.sem)
        att_class=Attendance.objects.filter(enrollment=student,sem=student.sem,attend=1).count()
        total_class=Attendance.objects.filter(enrollment=student,sem=student.sem).count()
        attendance = 0
        if total_class >0:
            attendance = round(att_class / total_class * 100, 2)
            cta = math.ceil((0.75*total_class - att_class)/0.25)
        if cta < 0:
            cta=0
        return render(request,'students/manage/attendance/student_attendance_view.html',{'student':student,'attend':attend,'total_class':total_class,'att_class':att_class,'attendance':attendance,'cta':cta})
    else:
        messages.error(request,"attendance not found !")
        return render(request,'students/manage/attendance/student_attendance_view.html',{'student':student})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_subject(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    teacher=User.objects.get(username=request.user.username)
    Subject=[]
    
    if Class.objects.filter(year=bat,branch=dept).exists():
        classes=Class.objects.filter(year=bat,branch=dept)
        for c in classes:
            if AssignCT.objects.filter(teacher_id=teacher,class_id=c).exists():
                a=AssignCT.objects.filter(teacher_id=teacher,class_id=c)
                Subject.append(a)
          
            else:
                pass
       
        return render(request,'teacher/teacher_subject.html',{'subject':Subject})
    



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def subject_attendance(request,sem,sec,subject_code):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    batc=batch.objects.latest('batch')
    bat=int(batc.batch)-x
    bats=get_object_or_404(batch,batch=bat)
    if request.method=='POST':
        subject_id=get_object_or_404(Subject_sem,year=batc,dept=dept,sem=sem,subject_code=subject_code)
        
        date=request.POST['date']
        if TeacherSubjectAttendance.objects.filter(subject_id=subject_id,date=date).exists():
            messages.error(request,'Attendance are already marked on given date')
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_subject_attendance.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
   
        else:
            if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
                student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
                for i in student:
                    s=Student.objects.get(enrollment=i.enrollment)
                    attend=request.POST[i.enrollment]
                    a=TeacherSubjectAttendance.objects.create(student_id=i,subject_id=subject_id,date=date,attend=attend)
                    a.save()
                messages.success(request,'Attendance marked sucessfully')
                return redirect('teacher_subject')
            else:
                messages.error(request,'student not found !')
                return redirect('teacher_subject')   
            
    else:
        subject_id=get_object_or_404(Subject_sem,year=batc,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_subject_attendance.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
        else:
            messages.error(request,'Student not found')  
            return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def subject_attendance_view(request,sem,sec,subject_code):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    batc=batch.objects.latest('batch')
    bat=int(batc.batch)-x
    bats=get_object_or_404(batch,batch=bat)
    subject_id=get_object_or_404(Subject_sem,year=batc,dept=dept,sem=sem,subject_code=subject_code)
    
    if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
        student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
        object_list=[]
        for s in student:
            stu=Student.objects.get(enrollment=s.enrollment)
            if TeacherSubjectAttendance.objects.filter(student_id=stu,subject_id=subject_id).exists():
                att_class = TeacherSubjectAttendance.objects.filter(student_id=stu,subject_id=subject_id,attend=1).count()
                total_class =TeacherSubjectAttendance.objects.filter(student_id=stu,subject_id=subject_id).count()
                attendance = 0
                if total_class!=0:
                    attendance = round(att_class / total_class * 100, 2)
            
                cta = math.ceil((0.75*total_class - att_class)/0.25)
                if cta < 0:
                    cta=0
                data=[stu,att_class,total_class,attendance,cta]
                object_list.append(data)
            else:
                messages.error(request,"attendance not found!")
                return redirect('teacher_subject')
        return render(request,'teacher/teacher_subject_attendance_view.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id,'object_list':object_list})
    else:
        messages.error(request,'Student not found')  
        return redirect('teacher_subject')


def subject_attendance_details(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        subject_id=request.POST['subject_id']
        subject=get_object_or_404(Subject_sem,year=bat,dept=dept,subject_code=subject_id)
        if TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=subject).exists():
            attendance=TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=subject)
            return render(request,'teacher/subject_attendance_details.html',{'attend':attendance,'student':student,'subject':subject}) 
        else:
            return render(request,'teacher/subject_attendance_details.html') 
    

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def subject_attendance_update(request,pk,subject_code,date):
    student=get_object_or_404(Student,enrollment=pk)       
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    subject=get_object_or_404(Subject_sem,year=bat,dept=dept,subject_code=subject_code)
    attend=get_object_or_404(TeacherSubjectAttendance,student_id=student,subject_id=subject,date=date)
    if request.method=='POST':
        status=request.POST[student.enrollment]
        if TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=subject,date=date).exists():
            attend=TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=subject,date=date).update(attend=status)
            attendance=TeacherSubjectAttendance.objects.filter(student_id=student,subject_id=subject)
            messages.success(request,'Attendance Updated successfully')
            return render(request,'teacher/subject_attendance_details.html',{'attend':attendance,'student':student,'subject':subject}) 
        else:
            messages.error(request,"attendance not found")
            return redirect('teacher_subject')
    return render(request,'teacher/subject_attendance_update.html',{'date':date,'student':student,'subject':subject})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_subject_mark(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=get_object_or_404(batch,batch=bat)
    if request.method=='POST':
        exam_type=request.POST['exam_type']
        exam_no=request.POST['exam_no']
        unit_no=request.POST['unit_no']
        total_mark=request.POST['total_mark']
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            for s in student:
                obtain_mark=request.POST[s.enrollment]
                if TeacherSubjectMark.objects.filter(student_id=s,subject_id=subject_id,exam_type=exam_type,exam_no=exam_no,unit_no=unit_no).exists():
                    messages.error(request," Already  Marked")
                    return render(request,'teacher/teacher_subject_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
                else:
                    m=TeacherSubjectMark.objects.create(student_id=s,subject_id=subject_id,exam_type=exam_type,exam_no=exam_no,unit_no=unit_no,total_mark=total_mark,obtain_mark=obtain_mark)
                    m.save()
            messages.success(request,"Marked Successfully")
            return redirect('teacher_subject')
        else:
            messages.error(request,"Student not found !")
            return redirect('teacher_student')
    else:
    
        subject_id=get_object_or_404(Subject_sem,year=bats,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_subject_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
        else:
            messages.error(request,'Student not found')  
            return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_unit_mark_view(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=batch.objects.get(batch=bat)
    if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
        student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        return render(request,'teacher/teacher_unit_mark_view.html',{'student':student,'subject_id':subject_id,'sem':sem,'sec':sec})
    else:
        messages.error(request,'Student not found')
        return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_unit_mark_view(request,pk,subject_code):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='tutorial')
        mark1=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='test')
        return render(request,'teacher/teacher_student_unit_mark_view.html',{'mark':mark,'mark1':mark1,'subject_id':subject_id,'student':student})
    else:
        messages.error(request,'marks not found')
        return redirect('teacher_practical_mark_view',subject_code=subject_code,sem=student.sem,sec=student.sec)



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_unit_mark_update(request,pk,subject_code,exam_type,exam_no,unit_no):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    
    subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if request.method=='POST':
  
        obtain_mark=request.POST['obtain_mark']
        if TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type=exam_type,exam_no=exam_no,unit_no=unit_no).exists():
            TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type=exam_type,exam_no=exam_no,unit_no=unit_no).update(obtain_mark=obtain_mark)
            messages.success(request,'marks updated successfully')
            return redirect('teacher_student_unit_mark_view',pk=pk,subject_code=subject_code)
        else:
            messages.error(request,'marks not found')
            return redirect('teacher_student_unit_mark_view.html',pk=pk,subject_code=subject_code)
    else:
        return render(request,'teacher/teacher_student_unit_mark_update.html',{'subject_id':subject_id,'student':student,'exam_no':exam_no,'exam_type':exam_type,'unit_no':unit_no})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_subject_midterm(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=get_object_or_404(batch,batch=bat)
    if request.method=='POST':
        exam_no=request.POST['exam_no']
        total_mark=request.POST['total_mark']
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            for s in student:
                obtain_mark=request.POST[s.enrollment]
                if TeacherSubjectMidTerm.objects.filter(student_id=s,subject_id=subject_id,exam_no=exam_no).exists():
                    messages.error(request," Already  Marked")
                    return render(request,'teacher/teacher_subject_midterm.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
                else:
                    m=TeacherSubjectMidTerm.objects.create(student_id=s,subject_id=subject_id,exam_no=exam_no,total_mark=total_mark,obtain_mark=obtain_mark)
                    m.save()
            messages.success(request,"Marked Successfully")
            return redirect('teacher_subject')
        else:
            messages.error(request,"student not found !")
            return redirect('teacher_subject')
    else:
      
        subject_id=Subject_sem.objects.get(year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_subject_midterm.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
        else:
            messages.error(request,"student not found")
            return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_subject_midterm_view(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=batch.objects.get(batch=bat)
    if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
        student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        midterm1=[]
        midterm2=[]
        for s in student:
            mid=[]
            mid3=[]
            mid.append(s)
            mid3.append(s)
            if TeacherSubjectMidTerm.objects.filter(student_id=s,subject_id=subject_id,exam_no=1).exists():
                mid1=TeacherSubjectMidTerm.objects.get(student_id=s,subject_id=subject_id,exam_no=1)
                mid.append(mid1)
            else:
                mid.append(0)
            midterm1.append(mid)
            if TeacherSubjectMidTerm.objects.filter(student_id=s,subject_id=subject_id,exam_no=2).exists():
                mid2=TeacherSubjectMidTerm.objects.get(student_id=s,subject_id=subject_id,exam_no=2)
                mid3.append(mid2)
            else:
                mid3.append(0)
            midterm2.append(mid3)
        return render(request,'teacher/teacher_subject_midterm_view.html',{'subject':subject_id,'midterm1':midterm1,'midterm2':midterm2,'sem':sem,'sec':sec})
    else:
        messages.error(request,"Student not found")
        return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_subject_midterm_update(request,pk,subject_code,exam_no):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if request.method=='POST':
        obtain_mark=request.POST['obtain_mark']
        if TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id,exam_no=exam_no).exists():
            mid1=TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id,exam_no=1).update(obtain_mark=obtain_mark)
            messages.success(request,"marks updated successfully")
            return redirect('teacher_subject_midterm_view',subject_code=subject_code,sem=student.sem ,sec=student.sec)
        else:
            messages.error(request,"marks not found ")
            return redirect('teacher_subject_midterm_view',subject_code=subject_code,sem=student.sem ,sec=student.sec)
    return render(request,'teacher/teacher_subject_midterm_update.html',{'student':student,'subject':subject_id,'exam_no':exam_no})





@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_practical_mark(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=get_object_or_404(batch,batch=bat)
    if request.method=='POST':
        practical_no=request.POST['practical_no']
        total_mark=request.POST['total_mark']
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            for s in student:
                obtain_mark=request.POST[s.enrollment]
                if TeacherPracticalMark.objects.filter(student_id=s,subject_id=subject_id,practical_no=practical_no).exists():
                    messages.success(request," Already  Marked")
                    return render(request,'teacher/teacher_practical_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
                else:
                    m=TeacherPracticalMark.objects.create(student_id=s,subject_id=subject_id,practical_no=practical_no,total_mark=total_mark,obtain_mark=obtain_mark)
                    m.save()
            messages.success(request,"Marked Successfully")
            return redirect('teacher_subject')
        else:
            messages.error(request,"student not found !")
            return redirect('teacher_subject')
    else:
      
        subject_id=Subject_sem.objects.get(year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_practical_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
        else:
            messages.error(request,"student not found")
            return redirect('teacher_subject')
   

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_practical_mark_view(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=batch.objects.get(batch=bat)
    if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
        student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        return render(request,'teacher/teacher_practical_mark_view.html',{'student':student,'subject_id':subject_id,'sem':sem,'sec':sec})
    else:
        messages.error(request,'Student not found')
        return redirect('teacher_subject')

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_practical_mark_view(request,pk,subject_code):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    
    subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'teacher/teacher_student_practical_mark_view.html',{'mark':mark,'subject_id':subject_id,'student':student})
    else:
        messages.error(request,'marks not found')
        return redirect('teacher_practical_mark_view',subject_code=subject_code,sem=student.sem,sec=student.sec)

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')

def teacher_student_practical_mark_update(request,pk,subject_code,practical_no):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    
    subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if request.method=='POST':
        obtain_mark=request.POST['obtain_mark']
        if TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id,practical_no=practical_no).exists():
            TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id,practical_no=practical_no).update(obtain_mark=obtain_mark)
            messages.success(request,'marks updated successfully')
            return redirect('teacher_student_practical_mark_view',pk=pk,subject_code=subject_code)
        else:
            messages.error(request,'marks not found')
            return redirect('teacher_student_practical_mark_view.html',pk=pk,subject_code=subject_code)
    else:
        return render(request,'teacher/teacher_student_practical_mark_update.html',{'subject_id':subject_id,'student':student,'practical_no':practical_no})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_project_mark(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=batch.objects.get(batch=bat)
    if request.method=='POST':
       
        total_mark=request.POST['total_mark']
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            for s in student:
                obtain_mark=request.POST[s.enrollment]
                if TeacherProjectMark.objects.filter(student_id=s,subject_id=subject_id).exists():
                    messages.error(request," Already  Marked")
                    return render(request,'teacher/teacher_project_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})
                else:
                    m=TeacherProjectMark.objects.create(student_id=s,subject_id=subject_id,total_mark=total_mark,obtain_mark=obtain_mark)
                    m.save()
            messages.success(request,"Marked Successfully")
            return redirect('teacher_subject')
        else:
            messages.error(request,'Student not found !')
            return redirect('teacher_subject')
    else:
      
        subject_id=Subject_sem.objects.get(year=bat,dept=dept,sem=sem,subject_code=subject_code)
        if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
            student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
            return render(request,'teacher/teacher_project_mark.html',{'student':student,'sem':sem,'sec':sec,'subject_id':subject_id})

        else:
            messages.error(request,"student not found")
            return redirect('teacher_subject')
    

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_project_mark_view(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    x=int(sem)//2
    bat=batch.objects.latest('batch')
    bat=int(bat.batch)-x
    bats=batch.objects.get(batch=bat)
    if Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec).exists():
        student=Student.objects.filter(batch=bats,branch=dept,sem=sem,sec=sec)
        bat=batch.objects.latest('batch')
        subject_id=get_object_or_404(Subject_sem,year=bat,dept=dept,sem=sem,subject_code=subject_code)
        mark=[]
        
        for s in student:
            if TeacherProjectMark.objects.filter(student_id=s,subject_id=subject_id).exists():
                m=TeacherProjectMark.objects.get(student_id=s,subject_id=subject_id)
                mark.append(m)
            else:
                messages.error(request,'Marks not found')
                return redirect('teacher_subject')
        return render(request,'teacher/teacher_project_mark_view.html',{'subject_id':subject_id,'sem':sem,'sec':sec,'mark':mark})
    else:
        messages.error(request,'Student not found')
        return redirect('teacher_subject')

#tested

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_project_mark_update(request,pk,subject_code):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    student=get_object_or_404(Student,enrollment=pk)
    subject_id=Subject_sem.objects.get(year=bat,dept=dept,sem=student.sem,subject_code=subject_code)
    if request.method=='POST':
        
        obtain_mark=request.POST['obtain_mark']
        if TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
            TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id).update(obtain_mark=obtain_mark)
            messages.success(request,'marks updated successfully')
            return redirect('teacher_project_mark_view',subject_code=subject_code,sem=student.sem,sec=student.sec)
        else:
            messages.error(request,'marks not found !')
            return redirect('teacher_project_mark_view',subject_code=subject_code,sem=student.sem,sec=student.sec)
    else:
        return render(request,'teacher/teacher_project_mark_update.html',{'subject_id':subject_id,'student':student})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def teacher_student_list(request,pk):
    dept=request.user.profile.department
    query=request.GET.get('query')
    if query==None:
        query=''
    if len(query)>100:
        messages.warning(request,"Your Query is too long ............ ")
        return render(request,'students/manage/student/teacher_student_list.html')

    if Student.objects.filter(owner=request.user,branch=dept).exists():
        batch_list=Student.objects.filter(owner=request.user).values('batch')
        batch={item['batch'] for item in batch_list}
       
        all_student=[]
        for b in batch:
            student=Student.objects.filter(batch=b,branch=dept,owner=request.user).filter(Q(enrollment__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
            all_student.append(student)
        if len(all_student)==0:
            messages.error(request,'No Result found !')
            return render(request,'students/manage/student/teacher_student_list.html',{'all_student':all_student})
        return render(request,'students/manage/student/teacher_student_list.html',{'all_student':all_student})
    else:
        messages.error(request,'Student Not found')
        return redirect('teacher_dash')


    
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def tg_student_attendance(request):
    p_pickoff=datetime.datetime.now().date()+timedelta(days=1)
    p_pickup=datetime.datetime.now().date()-timedelta(days=7)
    
    dept=request.user.profile.department
 
    if Student.objects.filter(owner=request.user,branch=dept).exists():
        batch_list=Student.objects.filter(owner=request.user,active=True).values('batch')
        batch={item['batch'] for item in batch_list}
        all_attendance=[]
        for b in batch:
            att=[]
            student=Student.objects.filter(batch=b,branch=dept,owner=request.user)
            for s in student:
                if TotalAttendance.objects.filter(enrollment=s,sem=s.sem).exists():
                    a=TotalAttendance.objects.get(enrollment=s,sem=s.sem)
                    
                    att.append(a)
                else:
                    x=TotalAttendance.objects.create(enrollment=s,sem=s.sem)
                    x.save()
                    a=TotalAttendance.objects.get(enrollment=s,sem=s.sem)
                    att.append(a)
            all_attendance.append(att)
        return render(request,'students/manage/TgAttendance/tg_student_attendance.html',{'object_list':all_attendance,'p_pickup':p_pickup,'p_pickoff':p_pickoff})
    else:
        messages.error(request,'Student not fopund !')
        return redirect('teacher_dash')


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def tg_student_attendance_date(request):
   
    dept=request.user.profile.department
    pickup=request.GET.get('date__gte','None');
    dropoff=request.GET.get('date__lt','None');
    if Student.objects.filter(owner=request.user,branch=dept).exists():
        batch_list=Student.objects.filter(owner=request.user,active=True).values('batch')
        batch={item['batch'] for item in batch_list}
        all_attendance=[]
        for b in batch:
            att=[]
            student=Student.objects.filter(batch=b,branch=dept,owner=request.user)
            for s in student:
                stu=Student.objects.get(enrollment=s.enrollment)
                if Attendance.objects.filter(enrollment=s,sem=s.sem).exists():
                    w=Attendance.objects.filter(sem=s.sem).latest('week')
                    w=w.week
                    att_class=Attendance.objects.filter(enrollment=s,sem=s.sem,attend=1).filter(date__range=(pickup,dropoff)).count()     
                    total_class=Attendance.objects.filter(enrollment=s,sem=s.sem).filter(date__range=(pickup,dropoff)).count()
                    attendance = 0
                    if total_class >0:
                        attendance = round(att_class / total_class * 100, 2)
                    cta = math.ceil((0.75*total_class - att_class)/0.25)
                    if cta < 0:
                        cta=0
                    att.append([stu,att_class,total_class,attendance,cta])
                else:
                    att.append([stu,0,0,0,0])    
            all_attendance.append([att,b])
       
        return render(request,'students/manage/TgAttendance/tg_student_attendance_date.html',{'object_list':all_attendance,'pickup':pickup,'dropoff':dropoff})
    else:
        messages.error(request,'Student not fopund !')
        return redirect('teacher_dash')



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def tg_student_attendance_week(request):
   
    dept=request.user.profile.department
     

    if Student.objects.filter(owner=request.user,branch=dept).exists():
        batch_list=Student.objects.filter(owner=request.user,active=True).values('batch')
        batch={item['batch'] for item in batch_list}
        all_attendance=[]
        for b in batch:
            att=[]
            student=Student.objects.filter(batch=b,branch=dept,owner=request.user)
            for s in student:
                stu=Student.objects.get(enrollment=s.enrollment)
                if Attendance.objects.filter(enrollment=s,sem=s.sem).exists():
                    w=Attendance.objects.filter(sem=s.sem).latest('week')
                    w=w.week
                    att_class=Attendance.objects.filter(enrollment=s,sem=s.sem,week=w,attend=1).count()       
                    total_class=Attendance.objects.filter(enrollment=s,sem=s.sem,week=w).count()
                    attendance = 0
                    if total_class >0:
                        attendance = round(att_class / total_class * 100, 2)
                    cta = math.ceil((0.75*total_class - att_class)/0.25)
                    if cta < 0:
                        cta=0
                    att.append([stu,att_class,total_class,attendance,cta])
                else:
                    att.append([stu,0,0,0,0])    
            all_attendance.append([att,b])
       
        return render(request,'students/manage/TgAttendance/tg_student_attendance_week.html',{'object_list':all_attendance})
    else:
        messages.error(request,'Student not fopund !')
        return redirect('teacher_dash')












import requests



@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def attendance_notification(request,pk,message_type,attendance):
    student=get_object_or_404(Student,enrollment=pk)
    
    message=get_object_or_404(AttendanceMessages,message_type=message_type)
    text='Dear {0} {1} {2} {3} {4}'.format(student.first_name,student.last_name,student.enrollment,message.messages,attendance)
    
    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS& message={0} &language=english&route=p&numbers={1}".format(text,student.phone)
    headers = {
        'authorization': "ywkf54xDPTsrcEHalWN6ZLUnSX9u3bAmzCRdF2Jv1VBQ0hYIgqcZewgV678ukv5bqMrfh4zjsiIloynP",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        messages.success(request,response.text)
        return redirect('tg_student_attendance')
    except:
        messages.error(request,"check your internet connection..............")
        return redirect('tg_student_attendance')
    