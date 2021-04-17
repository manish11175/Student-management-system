import math
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.urls import	reverse_lazy 
from django.views.generic.edit	import	CreateView,	UpdateView,DeleteView
from django.views.generic.list	import	ListView
from student.models import	Student,StuMedical,Attendance,TotalAttendance
from student.models import  StuBank,StuHostel,StuBank,StuAdmission,Stu_placement,StuLocalGuard
from django.contrib.auth.mixins	import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import redirect,	get_object_or_404 
from django.views.generic.base	import	TemplateResponseMixin,	View 

from django.forms.models import	modelform_factory 
from django.apps	import	apps 
from django.db.models import Count 
from student.models import StudentResult,StudentMidsem,StudentFee,StudentAddress,StudentResident
from student.models import Student,batch,Family,Tgcalling,StudentEducation
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators	import	login_required
from hod.models import Subject_sem,TeacherSubjectAttendance,TeacherPracticalMark,TeacherProjectMark,TeacherSubjectMark,TeacherSubjectMidTerm
from django.contrib import messages
from student.forms import StudentSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter

def user_autherization(user):
    try:
        return user.studentprofile.role=='student'
    except ObjectDoesNotExist:
        pass


@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_dash(request):
    return render(request,'user/student_dash.html')

@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_profile(request):
    return render(request,'user/student_profile.html')

@user_passes_test(user_autherization,login_url='/account/student_login/')
def resident(request):
    student=get_object_or_404(Student,enrollment=request.user.username)
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
            return redirect('resident_update')
        else:
            s=StudentResident.objects.create(enrollment=student,house_no=house_no,street=street,city=city,district=district,\
                state=state,country=country,pincode=pincode)
            s.save()
            address=StudentResident.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/resident.html',{'student':student,'address':address})
    else:
        if  StudentResident.objects.filter(enrollment=student).exists():
            address=StudentResident.objects.get(enrollment=student)
            return render(request,'user/manage/resident.html',{'student':student,'address':address})
        else:
            return render(request,'user/manage/resident.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')
def resident_update(request):
    student=Student.objects.get(enrollment=request.user.username)
    if  StudentResident.objects.filter(enrollment=student.enrollment).exists():
        if request.method=='POST':
            house_no=request.POST['house_no']
            street=request.POST['street']
            city=request.POST['city']
            district=request.POST['district']
            state=request.POST['state']
            country=request.POST['country']
            pincode=request.POST['pincode']
            s=StudentResident.objects.filter(enrollment=student).update(house_no=house_no,street=street,country=country,district=district,state=state,pincode=pincode,city=city)
            messages.success(request,'resident updates successfully')
            return redirect('resident_update')
        return render(request,'user/manage/resident_update.html')
@user_passes_test(user_autherization,login_url='/account/student_login/')
def address(request):
    student=get_object_or_404(Student,enrollment=request.user.username)
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
            return render(request,'user/manage/address.html',{'student':student,'address':address})
     
    else:
        if  StudentAddress.objects.filter(enrollment=student).exists():
            address=StudentAddress.objects.get(enrollment=student)
            return render(request,'user/manage/address.html',{'student':student,'address':address})
        else:
            return render(request,'user/manage/address.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')  
def fee(request):
    student=Student.objects.get(enrollment=request.user.username)
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
        receipt=request.FILES['receipt']
        fee=StudentFee.objects.create(enrollment=student,sem=sem,total_amt=total_amt,amt_due=amt_due,amt_paid=amt_paid,receipt_no=receipt_no,date=date,receipt=receipt)
        fee.save()
        messages.success(request,'Fee Recorded Successfully')	
        object_list=StudentFee.objects.filter(enrollment=student.enrollment)
        return render(request,'user/manage/fee.html',{'student':student,'object_list':object_list})
    else:
        if  StudentFee.objects.filter(enrollment=student.enrollment).exists():
            object_list=StudentFee.objects.filter(enrollment=student.enrollment)
            return render(request,'user/manage/fee.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'user/manage/fee.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')
def midterm(request):
    student=Student.objects.get(enrollment=request.user.username)
    if request.method=='POST':
        sem=request.POST['sem']
        midterm=request.POST['midterm']
        total_mark=request.POST['total_mark']
        obtain_mark=request.POST['obtain_mark']
        obtain_mark=float(obtain_mark)
        total_mark=float(total_mark)
        avg=obtain_mark/(total_mark/100)
        if obtain_mark<total_mark:
            if StudentMidsem.objects.filter(enrollment=student,sem=sem,midterm=midterm).exists():
                messages.error(request,'marked already !')
                return redirect('midterm_update')
                
            else:
                result=StudentMidsem.objects.create(enrollment=student,sem=sem,midterm=midterm,total_mark=total_mark,obtain_mark=obtain_mark,avg=avg)
                result.save()
                object_list=StudentMidsem.objects.filter(enrollment=student.enrollment)
                messages.success(request,'Result Recorded Successfully')
                return render(request,'user/manage/midsem.html',{'object_list':object_list})
                
        else:
            messages.error(request,'obtain mark should be less than total mark')
            return redirect('/user/midterm/')
    else:
        if  StudentMidsem.objects.filter(enrollment=student.enrollment).exists():
            object_list=StudentMidsem.objects.filter(enrollment=student.enrollment)
            return render(request,'user/manage/midsem.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'user/manage/midsem.html')


@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_education(request):
    student=Student.objects.get(enrollment=request.user.username)
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
                return redirect('education')
                
            else:
                result=StudentEducation.objects.create(enrollment=student,course=course,roll_no=roll_no,rank=rank,board=board,year_of_passing=year_of_passing,total_mark=total_mark,obtain_mark=obtain_mark,percent=percent)
                result.save()
                object_list=StudentEducation.objects.filter(enrollment=student.enrollment)
                messages.success(request,'Response Recorded Successfully')
                return render(request,'user/manage/education.html',{'object_list':object_list})
                
        else:
            messages.error(request,'obtain mark should be less than total mark')
            return redirect('education')
    else:
        if  StudentEducation.objects.filter(enrollment=student.enrollment).exists():
            object_list=StudentEducation.objects.filter(enrollment=student.enrollment)
            return render(request,'user/manage/education.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'user/manage/education.html')
      

@user_passes_test(user_autherization,login_url='/account/student_login/')
def result(request):
    student=Student.objects.get(enrollment=request.user.username)
    if request.method=='POST':
        sem=request.POST['sem']
        result=request.POST['result']
        sgpa=request.POST['sgpa']
       
        cgpa=request.POST['cgpa']
        cgpa=int(cgpa)
        if_fail=request.POST['if_fail']
        marksheet=request.FILES['marksheet']
        if int(sgpa)<cgpa:
            if StudentResult.objects.filter(enrollment=student,sem=sem).exists():
                messages.error(request,'already recorded !')
                return redirect('result_update')
            else:
                result=StudentResult.objects.create(enrollment=student,sem=sem,result=result,sgpa=sgpa,cgpa=cgpa,if_fail=if_fail,marksheet=marksheet)
                result.save()
                object_list=StudentResult.objects.filter(enrollment=student.enrollment)
                messages.success(request,'Result Recorded Successfully')
                return render(request,'user/manage/result.html',{'student':student,'object_list':object_list})
        else:
            messages.error(request,'SGPA mark should be less than CGPA')
            return redirect('result_update')
    else:
        if StudentResult.objects.filter(enrollment=student.enrollment).exists():
            object_list=StudentResult.objects.filter(enrollment=student.enrollment)
            return render(request,'user/manage/result.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'user/manage/result.html')
    


@user_passes_test(user_autherization,login_url='/account/student_login/')
def placement(request):
    student=Student.objects.get(enrollment=request.user.username)
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
        object_list=Stu_placement.objects.filter(enrollment=student.enrollment)
        messages.success(request,'PLacement  Recorded Successfully')
        return render(request,'user/manage/placement.html',{'student':student,'object_list':object_list})
    
    else:
        if  Stu_placement.objects.filter(enrollment=student.enrollment).exists():
            object_list=Stu_placement.objects.filter(enrollment=student.enrollment)
            return render(request,'user/manage/placement.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'user/manage/placement.html',{'student':student})
        


@user_passes_test(user_autherization,login_url='/account/student_login/')
def admission(request):
    student=get_object_or_404(Student,enrollment=request.user.username)
    
    if request.method=='POST':
        entrance=request.POST['entrance']
        admisbase=request.POST['admisbase']
        sch_no=request.POST['sch_no']
        branch=request.POST['branch']
        sem=request.POST['sem']
        sec=request.POST['sec']
        year=request.POST['year']
        if StuAdmission.objects.filter(enrollment=student).exists():
            messages.error(request,"Alreay added !")
            return redirect('admission_update')
        else:
            a=StuAdmission.objects.create(enrollment=student,entrance=entrance,admisbase=admisbase,sch_no=sch_no\
                ,branch=branch,sem=sem,sec=sec,year=year)
            a.save()
            admission=StuAdmission.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/admission.html',{'student':student,'admission':admission})
       
    else:
        if  StuAdmission.objects.filter(enrollment=student).exists():
            admission=StuAdmission.objects.get(enrollment=student)
            return render(request,'user/manage/admission.html',{'student':student,'admission':admission})
        else:
            return render(request,'user/manage/admission.html',{'student':student})
            
@user_passes_test(user_autherization,login_url='/account/student_login/')      
def hostel(request):
    student=Student.objects.get(enrollment=request.user.username)
    
    if request.method=='POST':
        name_hostel=request.POST['name_hostel']
        room_no=request.POST['room_no']
        resi_address=request.POST['resi_address']
        pincode=request.POST['pincode']
      
        if StuHostel.objects.filter(enrollment=student).exists():
            messages.error(request,'hostel details already added !')
            return redirect('hostel_update')
        else:
            a=StuHostel.objects.create(enrollment=student,name_hostel=name_hostel,room_no=room_no,\
                resi_address=resi_address,pincode=pincode)
            a.save()
            hostel=StuHostel.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/hostel.html',{'student':student,'hostel':hostel})
        
    else:
        if  StuHostel.objects.filter(enrollment=student).exists():
            hostel=StuHostel.objects.get(enrollment=student)
            return render(request,'user/manage/hostel.html',{'student':student,'hostel':hostel})
        else:
            return render(request,'user/manage/hostel.html',{'student':student})


@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_sem_attendance(request):
    labels = []
    data = []
    student=Student.objects.get(enrollment=request.user)
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
            return render(request,'user/attendance/student_attendance.html',{'attend':attend,'att_class':att_class,'total_class':total_class,'attendance':attendance,'cta':cta, 'labels': labels,'data': data,})
        else:
            messages.error(request,"attendance not found !")
            return render(request,'user/attendance/student_attendance.html')
            
            
    else:
        return render(request,'user/attendance/student_attendance.html')
    return render(request,'user/attendance/student_attendance.html')



@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_subject_attendance(request):
    student=Student.objects.get(enrollment=request.user)
    dept=request.user.studentprofile.department
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
                return render(request,'user/subject/subject_attendance.html',{'student':student,'object_list':object_list})
            else:
                messages.error(request,"you don't have attendance record")
                return render(request,'user/subject/subject_attendance.html')    
        else:
            messages.error(request,"Please Select the valid semester")
            return render(request,'user/subject/subject_attendance.html')
    return render(request,'user/subject/subject_attendance.html')

@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_subject(request):
    student=Student.objects.get(enrollment=request.user)
    dept=request.user.studentprofile.department
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
                
                return render(request,'user/subject/student_subject.html',{'subject':subject})
            else:
                messages.error(request,"subjects  not found")
                return redirect('student_subject')
        else:
            messages.error(request,"Please Select the valid semester")
            return redirect('student_subject')

    return render(request,'user/subject/student_subject.html')

    
@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_unit_mark(request,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=Student.objects.get(enrollment=request.user)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='tutorial')
        mark1=TeacherSubjectMark.objects.filter(student_id=student,subject_id=subject_id,exam_type='test')
        return render(request,'user/subject/student_unit_mark_view.html',{'mark':mark,'mark1':mark1,'subject_id':subject_id,'student':student})
    else:
        messages.error(request,'Unit marks nor found !')
        return redirect('student_subject')

@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_midterm_mark(request,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=Student.objects.get(enrollment=request.user)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherSubjectMidTerm.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'user/subject/student_midterm_view.html',{'mark':mark,'student':student,'subject':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('student_subject')
        

@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_practical_mark(request,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=Student.objects.get(enrollment=request.user)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherPracticalMark.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'user/subject/student_practical_mark_view.html',{'mark':mark,'student':student,'subject':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('student_subject')
        


@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_project_mark(request,year,sem,subject_code):
    bat=get_object_or_404(batch,batch=year)
    student=Student.objects.get(enrollment=request.user)
    subject_id=get_object_or_404(Subject_sem,subject_code=subject_code,year=bat,sem=sem,dept=student.branch)
    
    if TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id).exists():
        mark=TeacherProjectMark.objects.filter(student_id=student,subject_id=subject_id)
        return render(request,'user/subject/student_project_mark_view.html',{'mark':mark,'student':student,'subject_id':subject_id})

    else:
        messages.error(request,'marks nor found !')
        return redirect('student_subject')
        


























# Student Personal Information
@user_passes_test(user_autherization,login_url='/account/student_login/')
def family(request):
    student=Student.objects.get(enrollment=request.user.username)
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
            return redirect('family_update')
        else:
            f=Family.objects.create(enrollment=student,father_name=father_name,father_mob=father_mob,father_email=father_email,father_organi=father_organi,\
                father_occup=father_occup,father_income=father_income,father_office=father_office,mother_name=mother_name,mother_mob=mother_mob,mother_email=mother_email,\
                    mother_organi=mother_organi,mother_occup=mother_occup,mother_income=mother_income,mother_office=mother_office)
            f.save()
            family=Family.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/family.html',{'student':student,'family':family})
            
        
    else:
        if Family.objects.filter(enrollment=student).exists():
            family=Family.objects.get(enrollment=student)
            return render(request,'user/manage/family.html',{'student':student,'family':family})
        else:
            return render(request,'user/manage/family.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')
def lg(request):
    student=Student.objects.get(enrollment=request.user.username)
    if request.method=='POST':
        lg_name=request.POST['lg_name']
        lg_mob=request.POST['lg_mob']
        lg_address=request.POST['lg_address']
        stu_lg=request.POST['stu_lg']
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('lg_update')
        else:
            s=StuLocalGuard.objects.create(enrollment=student,local_guard_name=lg_name,guard_mob=lg_mob,\
                guard_address=lg_address,stu_rela_guard=stu_lg)
            s.save()
            lg=StuLocalGuard.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/lg.html',{'student':student,'lg':lg})
     
    else:
        if  StuLocalGuard.objects.filter(enrollment=student.enrollment).exists():
            lg=StuLocalGuard.objects.get(enrollment=student.enrollment)
            return render(request,'user/manage/lg.html',{'student':student,'lg':lg})
        else:
            return render(request,'user/manage/lg.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')
def medical(request):
    student=Student.objects.get(enrollment=request.user.username)
    if request.method=='POST':
        blood_group=request.POST['blood_group']
        physical=request.POST['physical']
        other=request.POST['other']
        if StuMedical.objects.filter(enrollment=student).exists():
            messages.error(request,'Already added')
            return redirect('medical_update')
        else:
            s=StuMedical.objects.create(enrollment=student,blood_group=blood_group,physical_disable=physical,other_med=other)
            s.save()
            medical=StuMedical.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/medical.html',{'student':student,'medical':medical})
    else:
        if  StuMedical.objects.filter(enrollment=student.enrollment).exists():
            medical=StuMedical.objects.get(enrollment=student.enrollment)
            return render(request,'user/manage/medical.html',{'student':student,'medical':medical})
        else:
            return render(request,'user/manage/medical.html',{'student':student})




@user_passes_test(user_autherization,login_url='/account/student_login/')
def bank(request):
    student=Student.objects.get(enrollment=request.user.username)
    if request.method=='POST':
        bank_name=request.POST['bank_name']
        bank_branch=request.POST['bank_branch']
        bank_ac=request.POST['bank_ac']
        bank_ifsc=request.POST['bank_ifsc']
        ac_hold_name=request.POST['ac_hold_name']
        aadhar_no=request.POST['aadhar_no']
        if StuBank.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('bank_update')
        else:
            s=StuBank.objects.create(enrollment=student,bank_name=bank_name,bank_branch=bank_branch,bank_ac=bank_ac,bank_ifsc=bank_ifsc,\
                ac_hold_name=ac_hold_name,aadhar_no=aadhar_no)
            s.save()
            bank=StuBank.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'user/manage/bank.html',{'student':student,'bank':bank})
    else:
        if  StuBank.objects.filter(enrollment=student.enrollment).exists():
            bank=StuBank.objects.get(enrollment=student.enrollment)
            return render(request,'user/manage/bank.html',{'student':student,'bank':bank})
        else:
            return render(request,'user/manage/bank.html',{'student':student})

@user_passes_test(user_autherization,login_url='/account/student_login/')
def student_tgcall(request):
    if Tgcalling.objects.filter(enrollment=request.user.username).exists():
        object_list=Tgcalling.objects.filter(enrollment=request.user.username)
        return render(request,'user/manage/tgcall.html',{'object_list':object_list})
    else:
        messages.error(request,'No Tgcalls foound !')
        return redirect('student_dash')
