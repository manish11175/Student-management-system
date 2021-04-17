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
from student.models import	Student,StuMedical,Family,StudentAddress,Stu_placement,Tgcalling,StudentResident,StuAdmission
from student.models import  StuBank,StuHostel,StudentFee,StudentMidsem,StudentResult,StudentEducation,StuLocalGuard,AttendanceMessages,batch
from django.forms.models import	modelform_factory 
from django.apps	import	apps 
from django.db.models import Count 
from student.models import StudentResult,StudentMidsem,StudentFee,StudentAddress,StudentResident
import math
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators	import	login_required
from account.models import Profile
from django.contrib import messages
from student.forms import StudentSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.contrib.auth.models import User,auth
from reportlab.pdfgen import canvas
from io import BytesIO
from django.db.models import Q
from myproject.utils import render_to_pdf
from.models import Class,Subject_sem,Syllabus,AssignCT,TutorGuard,TeacherSubjectAttendance

def hod_autherization(user):
    try:
        return user.profile.designation=='hod'
    except ObjectDoesNotExist:
        pass


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_dash(request):
    return render(request,'hod/hod_dash.html')
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_profile(request):
    return render(request,'hod/hod_profile.html')


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_subject_attendance(request,pk):
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
                return render(request,'hod/student/subject_attendance.html',{'student':student,'object_list':object_list})
            else:
                messages.error(request,"you don't have attendance record")
                return render(request,'hod/student/subject_attendance.html',{'student':student})    
        else:
            messages.error(request,"Please Select the valid semester")
            return render(request,'hod/student/subject_attendance.html',{'student':student})
    return render(request,'hod/student/subject_attendance.html',{'student':student})



@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_sem_attendance(request,pk):
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
            return render(request,'hod/student/student_attendance.html',{'attend':attend,'att_class':att_class,'total_class':total_class,'attendance':attendance,'cta':cta, 'labels': labels,'data': data,'student':student})
        else:
            messages.error(request,"attendance not found !")
            return render(request,'hod/student/student_attendance.html',{'student':student})
            
            
    else:
        return render(request,'hod/student/student_attendance.html',{'student':student})




@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone=request.POST['phone']
        if Student.objects.filter(enrollment=pk).exists():
            Student.objects.filter(enrollment=pk).update(Email=email,first_name=first_name,last_name=last_name,phone=phone) 
            messages.success(request,"updated successfully")
            return redirect('hod_student_view',pk=pk)
        else:
            message.error(request,'something went wrong !')
            return redirect('hod_student_view',pk=pk)
    return render(request,'hod/student/student_edit.html',{'student':student})

import requests



@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_attendance_notification(request,pk,message_type,attendance):
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
        return redirect('hod_student_attendance',pk=pk)
    except:
        messages.error(request,'Check your internet connection......')
        return redirect('hod_student_attendance',pk=pk)
 
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_attendance(request,pk):
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
        return render(request,'hod/student/student_attendance_view.html',{'student':student,'attend':attend,'total_class':total_class,'att_class':att_class,'attendance':attendance,'cta':cta})
    else:
        messages.error(request,"attendance not found !")
        return redirect('hod_student_attendance',pk=student.enrollment)
            
    return render(request,'hod/student/student_attendance_view.html',{'student':student})


# student medical details
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_medical(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        blood_group=request.POST['blood_group']
        physical=request.POST['physical']
        other=request.POST['other']
        if StuMedical.objects.filter(enrollment=student).exists():
            messages.error(request,'Already added')
            return redirect('hod_student_medical',pk=student.enrollment)
        else:
            s=StuMedical.objects.create(enrollment=student,blood_group=blood_group,physical_disable=physical,other_med=other)
            s.save()
            medical=StuMedical.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'hod/student/teacher_student_medical.html',{'medical':medical,'student':student})
    else:
        if StuMedical.objects.filter(enrollment=student).exists():
            medical=StuMedical.objects.get(enrollment=student)
            return render(request,'hod/student/teacher_student_medical.html',{'medical':medical,'student':student})
        else:
            return render(request,'hod/student/teacher_student_medical.html',{'student':student})

# student bank details

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_bank(request,pk):
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
            return redirect('hod_student_bank',pk=student.enrollment)
        else:
            s=StuBank.objects.create(enrollment=student,bank_name=bank_name,bank_branch=bank_branch,bank_ac=bank_ac,bank_ifsc=bank_ifsc,\
                ac_hold_name=ac_hold_name,aadhar_no=aadhar_no)
            s.save()
            bank=StuBank.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'hod/student/teacher_student_bank.html',{'bank':bank,'student':student})
    else:
        if StuBank.objects.filter(enrollment=student).exists():
            bank=StuBank.objects.get(enrollment=student)
            return render(request,'hod/student/teacher_student_bank.html',{'bank':bank,'student':student})
        else:
            return render(request,'hod/student/teacher_student_bank.html',{'student':student})


#Adding details about the student local guardian

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_lg(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        lg_name=request.POST['lg_name']
        lg_mob=request.POST['lg_mob']
        lg_address=request.POST['lg_address']
        stu_lg=request.POST['stu_lg']
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            messages.error(request,'Already Exists')
            return redirect('hod_student_lg',pk=student.enrollment)
        else:
            s=StuLocalGuard.objects.create(enrollment=student,local_guard_name=lg_name,guard_mob=lg_mob,\
                guard_address=lg_address,stu_rela_guard=stu_lg)
            s.save()
            lg=StuLocalGuard.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'hod/student/teacher_student_lg.html',{'lg':lg,'student':student})
    else:
        if StuLocalGuard.objects.filter(enrollment=student).exists():
            lg=StuLocalGuard.objects.get(enrollment=student)
            return render(request,'hod/student/teacher_student_lg.html',{'lg':lg,'student':student})
        else:
            return render(request,'hod/student/teacher_student_lg.html',{'student':student})


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_lg_edit(request,pk):
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
            return render(request,'hod/student/teacher_student_lg.html',{'lg':lg,'student':student})
            
        else:
            messages.error(request,'Details not Found !')
            return redirect('hod_student_lg',pk=student.enrollment)
            
    return render(request,'hod/student/teacher_student_lg_edit.html',{'student':student})

#Adding details about the student family
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_family(request,pk):
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
            return redirect('hod_student_family',pk=student.enrollment)
        else:
            f=Family.objects.create(enrollment=student,father_name=father_name,father_mob=father_mob,father_email=father_email,father_organi=father_organi,\
                father_occup=father_occup,father_income=father_income,father_office=father_office,mother_name=mother_name,mother_mob=mother_mob,mother_email=mother_email,\
                    mother_organi=mother_organi,mother_occup=mother_occup,mother_income=mother_income,mother_office=mother_office)
            f.save()
            family=Family.objects.get(enrollment=student)
            messages.success(request,'added successfully')
            return render(request,'hod/student/teacher_student_family.html',{'family':family,'student':student})
            
    else:
        if Family.objects.filter(enrollment=student).exists():
            family=Family.objects.get(enrollment=student)
            return render(request,'hod/student/teacher_student_family.html',{'family':family,'student':student})
        else:
            return render(request,'hod/student/teacher_student_family.html',{'student':student})

#Addinng Student Fee
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_fee_update(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
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
            return redirect('hod_student_fee_update',pk=student.enrollment)
        else:
            fee=StudentFee.objects.create(enrollment=student,sem=sem,total_amt=total_amt,amt_due=amt_due,amt_paid=amt_paid,receipt_no=receipt_no,date=date)
            fee.save()
            messages.success(request,'Fee Recorded Successfully')	
            return redirect('hod_student_fee_update',pk=student.enrollment)
    else:
        if StudentFee.objects.filter(enrollment=student).exists():
            fee=StudentFee.objects.filter(enrollment=student)
            return render(request,'hod/student/student_fee.html',{'object_list':fee,'student':student})
        else:
            return render(request,'hod/student/student_fee.html',{'student':student})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_fee_edit(request,pk,receipt):
    student=get_object_or_404(Student,enrollment=pk)
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
            return render(request,'hod/student/student_fee.html',{'object_list':fee,'student':student})
        else:
            messages.error(request,'Fees with this receipt no Not Found !')
            return redirect('hod_student_fee_update',pk=student.enrollment)
    else:
        if StudentFee.objects.filter(enrollment=student,receipt_no=receipt).exists():
            fee=StudentFee.objects.get(enrollment=student,receipt_no=receipt)
            return render(request,'hod/student/student_fee_edit.html',{'fee':fee,'student':student})
        else:
            return render(request,'hod/student/student_fee_edit.html',{'student':student})

        


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_education(request,pk):
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
                return redirect('hod_student_education',pk=student.enrollment)
                
            else:
                result=StudentEducation.objects.create(enrollment=student,course=course,roll_no=roll_no,rank=rank,board=board,year_of_passing=year_of_passing,total_mark=total_mark,obtain_mark=obtain_mark,percent=percent)
                result.save()
                object_list=StudentEducation.objects.filter(enrollment=student)
                messages.success(request,'Response Recorded Successfully')
                return render(request,'hod/student/teacher_student_education.html',{'object_list':object_list,'student':student})
                
        else:
            messages.error(request,'obtain mark should be less than total mark')
            return redirect('hod_student_education',pk=student.enrollment)
    else:
        if  StudentEducation.objects.filter(enrollment=student).exists():
            object_list=StudentEducation.objects.filter(enrollment=student)
            return render(request,'hod/student/teacher_student_education.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'hod/student/teacher_student_education.html',{'student':student})



# student Stu_placement
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_placement(request,pk):
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
        return redirect('hod_student_placement',pk=student.enrollment)
    else:
        if Stu_placement.objects.filter(enrollment=student).exists():
            placed=Stu_placement.objects.filter(enrollment=student)
            return render(request,'hod/student/student_placement.html',{'object_list':placed,'student':student})
        else:
            return render(request,'hod/student/student_placement.html',{'student':student})
					
       							
          


# student hostel details
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_hostel(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        name_hostel=request.POST['name_hostel']
        room_no=request.POST['room_no']
        resi_address=request.POST['resi_address']
        pincode=request.POST['pincode']
        if StuHostel.objects.filter(enrollment=student).exists():
            messages.error(request,"Already added !")
            return redirect('hod_student_hostel',pk=student.enrollment)
        else:
            a=StuHostel.objects.create(enrollment=student,name_hostel=name_hostel,room_no=room_no,\
                resi_address=resi_address,pincode=pincode)
            a.save()
            messages.success(request,'added successfully')
            return redirect('hod_student_hostel',pk=student.enrollment)
    else:
        if StuHostel.objects.filter(enrollment=student).exists():
            hostel=StuHostel.objects.get(enrollment=student)
            return render(request,'hod/student/student_hostel.html',{'hostel':hostel,'student':student})
        else:
            return render(request,'hod/student/student_hostel.html',{'student':student})
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_hostel_edit(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    if request.method=='POST':
        name_hostel=request.POST['name_hostel']
        room_no=request.POST['room_no']
        resi_address=request.POST['resi_address']
        pincode=request.POST['pincode']
        StuHostel.objects.filter(enrollment=student).update(name_hostel=name_hostel,room_no=room_no,\
            resi_address=resi_address,pincode=pincode)
        hostel=StuHostel.objects.get(enrollment=student)
        messages.success(request,'Update successfully')
        return render(request,'hod/student/student_hostel.html',{'hostel':hostel,'student':student})
    return render(request,'hod/student/student_hostel_edit.html',{'student':student})



#Adding details about the student addmission
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_admission(request,pk):
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
            return redirect('hod_student_admission',pk=student.enrollment)
            
        else:
            a=StuAdmission.objects.create(enrollment=student,entrance=entrance,admisbase=admisbase,sch_no=sch_no\
                ,branch=branch,sem=sem,sec=sec,year=year)
            a.save()
            messages.success(request,'added successfully')
            return redirect('hod_student_admission',pk=student.enrollment)
    else:
        if StuAdmission.objects.filter(enrollment=student).exists():
            admission=StuAdmission.objects.get(enrollment=student)
            return render(request,'hod/student/student_admission.html',{'admission':admission,'student':student})
        else:
            return render(request,'hod/student/student_admission.html',{'student':student})



@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_result(request,pk):
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
                return redirect('hod_student_result',pk=student.enrollment)
            else:
                result=StudentResult.objects.create(enrollment=student,sem=sem,result=result,sgpa=sgpa,cgpa=cgpa,if_fail=if_fail,marksheet=marksheet)
                result.save()
                object_list=StudentResult.objects.filter(enrollment=student)
                messages.success(request,'Result Recorded Successfully')	
                return render(request,'hod/student/student_result.html',{'object_list':object_list,'student':student})

        else:
            messages.error(request,'CGPA and SGPA must be less than 10')
            return redirect('hod_student_result',pk=student.enrollment)
    else:
        if StudentResult.objects.filter(enrollment=student).exists():
            object_list=StudentResult.objects.filter(enrollment=student)
            return render(request,'hod/student/student_result.html',{'object_list':object_list,'student':student})
        else:
            return render(request,'hod/student/student_result.html',{'student':student})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_result_edit(request,pk,sem):
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
                return render(request,'hod/student/student_result.html',{'object_list':object_list,'student':student})
            else:
                messages.error(request,'Result not found!')
                return redirect('hod_student_result',pk=student.enrollment)
        else:
            messages.error(request,'CGPA and SGPA must be less than 10')
            return redirect('hod_student_result_edit',pk=student.enrollment,sem=sem)
    return render(request,'hod/student/student_result_edit.html',{'student':student,'sem':sem})

#Addinng Student Mid sem result
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_midsem(request,pk):
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
                return redirect('hod_student_midsem',pk=student.enrollment)
            else:
                result=StudentMidsem.objects.create(enrollment=student,sem=sem,midterm=midterm,total_mark=total_mark,obtain_mark=obtain_mark,avg=avg)
                result.save()
                messages.success(request,'Result Recorded Successfully')	
                return redirect('hod_student_midsem',pk=student.enrollment)
        else:
            messages.error(request,'obtain mark must equal or less then total mark')
            return redirect('hod_student_midsem',pk=student.enrollment)
    else:
        if  StudentMidsem.objects.filter(enrollment=student).exists():
            object_list=StudentMidsem.objects.filter(enrollment=student)
            return render(request,'hod/student/student_midsem.html',{'object_list':object_list,'student':student})
        else:
            return render(request,'hod/student/student_midsem.html',{'student':student})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_midsem_edit(request,pk,sem,midterm):
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
                return render(request,'hod/student/student_midsem.html',{'object_list':object_list,'student':student})
            else:
                messages.error(request,'Result not found !')	
                return redirect('hod_student_midsem',pk=student.enrollment)

        else:
            messages.error(request,'obtain mark must equal or less then total mark')
            return redirect('hod_student_midsem_edit',pk=student.enrollment,sem=sem,midterm=midterm)
    return render(request,'hod/student/student_midsem_edit.html',{'student':student,'sem':sem,'midterm':midterm})












@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_tg_call(request,pk):
    student=get_object_or_404(Student,enrollment=pk)
    
    if request.method=='POST':
        date=request.POST['date']
        contact_no=request.POST['contact_no']
        contact_person=request.POST['contact_person']
        reason=request.POST['reason']
        description=request.POST['description']
        if Tgcalling.objects.filter(enrollment=student,date=date).exists():
            messages.error(request,'Call recorded already exists on given date')
            return redirect('hod_student_tg_call',student.enrollment)
        else:
            tgcall=Tgcalling.objects.create(enrollment=student,sem=student.sem,date=date,contact_no=contact_no,contact_person=contact_person,reason=reason,description=description,faculty=request.user)
            tgcall.save()
            object_list=Tgcalling.objects.filter(enrollment=student)
            messages.success(request,'Tgcall  Recorded Successfully')
            return render(request,'hod/student/tgcalling.html',{'student':student,'object_list':object_list})
       
   
    else:
        if Tgcalling.objects.filter(enrollment=student).exists():
            object_list=Tgcalling.objects.filter(enrollment=student)
            return render(request,'hod/student/tgcalling.html',{'student':student,'object_list':object_list})
        else:
            return render(request,'hod/student/tgcalling.html',{'student':student})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def hod_student_view(request,pk):
    if Student.objects.filter(enrollment=pk).exists():
        student=get_object_or_404(Student,enrollment=pk)
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
        return render(request,"hod/student/hod_student_view.html",{'student':student,'family':family,'resident':resident,'address':address})
        
    else:
        messages.error(request,'Student not found !')
        return redirect('department_student')





@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def department_faculty(request):
    faculty=Profile.objects.filter(department=request.user.profile.department,designation='faculty',activate=True)
    Faculty=[]
    for f in faculty:
        tea=User.objects.get(username=f.user)
        Faculty.append(tea)
    return  render(request,'hod/department_faculty.html',{'faculty':Faculty})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def faculty_account_request(request):
    faculty=Profile.objects.filter(department=request.user.profile.department,designation='faculty',activate=False)
    Faculty=[]
    for f in faculty:
        tea=User.objects.get(username=f.user)
        Faculty.append(tea)
    return  render(request,'hod/faculty_account_request.html',{'faculty':Faculty})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def faculty_account_activate(request):
    faculty=Profile.objects.filter(department=request.user.profile.department,designation='faculty',activate=False)
    Faculty=[]
    if request.method=='POST':
        for f in faculty:
            tea=User.objects.get(username=f.user)
            Faculty.append(tea)
            active=request.POST[tea.username]
            ac=Profile.objects.filter(user=tea).update(activate=active)
        
        messages.info(request,"Faculty account activated  successfully")    
        return redirect('department_faculty')
    return  render(request,'hod/faculty_account_request.html',{'faculty':Faculty})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def attendance_report(request):
    object_list=[]
    date=batch.objects.latest('batch')
    year=int(date.batch)
    for i in range(year,year-4,-1):
        attend_list=[]
        if Student.objects.filter(branch=request.user.profile.department,batch=i).exists():
            student=Student.objects.filter(branch=request.user.profile.department,batch=i)
            for s in student:
                stu=Student.objects.get(enrollment=s.enrollment)
                if TotalAttendance.objects.filter(enrollment=s,sem=s.sem).exists():
                    a=TotalAttendance.objects.get(enrollment=stu,sem=s.sem)
                    attend_list.append(a)
                else:
                    s=TotalAttendance.objects.create(enrollment=s,sem=s.sem)
                    s.save()
                    a=TotalAttendance.objects.get(enrollment=stu,sem=s.sem)
                    attend_list.append(a)
            object_list.append(attend_list)
        
    
    return render(request,'hod/attendance_report.html',{'object_list':object_list})
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def generate_attendance_pdf(request,year):
    
    student=Student.objects.filter(branch=request.user.profile.department,batch=year)
    attend_list=[]
    for s in student:
        if TotalAttendance.objects.filter(enrollment=s.enrollment,sem=s.sem).exists():
            a=TotalAttendance.objects.get(enrollment=s.enrollment,sem=s.sem)
            attend_list.append(a)
        else:
            s=TotalAttendance.objects.create(enrollment=s,sem=s.sem)
            s.save()
            a=TotalAttendance.objects.filter(enrollment=s,sem=s.sem)
            attend_list.append(a)
   
    try:
        return render_to_pdf('pdf/attendance_report_pdf.html', {'instance': attend_list})
    except:
        messages.info(request,'Please check your internet connection ......')
        return redirect('attendance_report')

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def download_attendance_pdf(request,year):
    department=request.user.profile.department
    student=Student.objects.filter(branch=request.user.profile.department,batch=year)
    attend_list=[]
    for s in student:
        if TotalAttendance.objects.filter(enrollment=s.enrollment,sem=s.sem).exists():
            a=TotalAttendance.objects.get(enrollment=s.enrollment,sem=s.sem)
            attend_list.append(a)
        else:
            s=TotalAttendance.objects.create(enrollment=s,sem=s.sem)
            s.save()
            a=TotalAttendance.objects.filter(enrollment=s,sem=s.sem)
            attend_list.append(a)
   
    
    try:
        pdf=render_to_pdf('pdf/attendance_report_pdf.html', {'instance': attend_list})
        response=HttpResponse(pdf,content_type='application/pdf')
        filename=str(department)+'_attendence_'+str(year)+'_batch.pdf'
        content="attachment; filename=%s"%(filename)
        response['Content-Disposition']=content
        return response
    except:
        messages.info(request,'Please check your internet connection ......')
        return redirect('attendance_report')

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def add_subject(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        sem=request.POST['sem']
        subject_name=request.POST['subject_name']
        subject_code=request.POST['subject_code']
        suject_type=request.POST['subject_type']
        if Subject_sem.objects.filter(year=bat,subject_code=subject_code).exists():
            messages.info(request,'Suject is already added with given subject code')
            return render(request,'hod/add_subject.html',{'bat':bat})
            
        else:
            s=Subject_sem.objects.create(year=bat,dept=dept,sem=sem,subject_name=subject_name,\
                subject_code=subject_code,subject_type=suject_type)
            s.save()
            messages.info(request,'Subject Added Successfully')
            return render(request,'hod/add_subject.html',{'bat':bat})

            
    return render(request,'hod/add_subject.html',{'bat':bat})



    

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def subject_view(request):
    dept=request.user.profile.department
    b=batch.objects.latest('batch')
    if request.method=="POST":
        year=request.POST['year']
        if batch.objects.filter(batch=year).exists():
            bat=batch.objects.get(batch=year)
            subject=[]
            
            for i in range(1,9):
                if Subject_sem.objects.filter(year=year,dept=dept,sem=i).exists():
                    s=Subject_sem.objects.filter(year=year,dept=dept,sem=i)
                    subject.append(s)
                else:
                    pass
            if year==b.batch:
                return render(request,'hod/subject/subject_viewc.html',{'subject':subject})
            else:
                return render(request,'hod/subject_view.html',{'subject':subject})
        else:
            messages.info(request,'This batch is not start yet please contact to admin to start this batch')
            return render(request,"hod/subject_view.html")   
    else:
        subject=[]
        for i in range(1,9):
            if Subject_sem.objects.filter(year=b.batch,dept=dept,sem=i).exists():
                s=Subject_sem.objects.filter(year=b.batch,dept=dept,sem=i)
                subject.append(s)
            else:
                pass
        return render(request,'hod/subject/subject_viewc.html',{'subject':subject})
       

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def subject_update(request,sem,subject_code):
    dept=request.user.profile.department
    year=batch.objects.latest('batch')
    if request.method=="POST":
        subject_name=request.POST['subject_name']
        subject_type=request.POST['subject_type']
        if Subject_sem.objects.filter(year=year,dept=dept,sem=sem,subject_code=subject_code).exists():
            Subject_sem.objects.filter(year=year,dept=dept,sem=sem,subject_code=subject_code).update(subject_name=subject_name,subject_type=subject_type)
            
            messages.info(request,"Subject updated Successfully")
            return redirect("subject_view")
        else:
            messages.info(request,"Subject not found")
            return redirect("subject_view")
    return render(request,'hod/subject/subject_update.html',{'year':year,'sem':sem,'subject_code':subject_code})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def subject_delete(request,sem,subject_code):
    dept=request.user.profile.department
    year=batch.objects.latest('batch')
    return render(request,'hod/subject/subject_delete.html',{'year':year,'sem':sem,'subject_code':subject_code})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def subject_delete_confirm(request,sem,subject_code):
    dept=request.user.profile.department
    year=batch.objects.latest('batch')
    if Subject_sem.objects.filter(year=year,dept=dept,sem=sem,subject_code=subject_code).exists():
        s=Subject_sem.objects.get(year=year,dept=dept,sem=sem,subject_code=subject_code)
        s.delete()
       
        subject=[]
        for i in range(1,9):
            if Subject_sem.objects.filter(year=year,dept=dept,sem=i).exists():
                s=Subject_sem.objects.filter(year=year,dept=dept,sem=i)
                subject.append(s)
            else:
                pass
        messages.info(request,"Subject Delete Successfully")
        return render(request,'hod/subject/subject_viewc.html',{'subject':subject})
    else:
        messages.info(request,"Subject not found")
        return redirect("subject_view")
    
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def syllabus(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=="POST":
        sem=request.POST['sem']
        file=request.FILES['file']
        if Syllabus.objects.filter(year=bat,dept=dept,sem=sem).exists():
            messages.info(request,'Syllabus already exists in this semester')
            return render(request,'hod/subject/syllabus.html',{'bat':bat})
        else:
            s=Syllabus.objects.create(year=bat,dept=dept,sem=sem,file=file)
            messages.info(request,'Syllabus added successfully')
            return render(request,'hod/subject/syllabus.html',{'bat':bat})
    return render(request,'hod/subject/syllabus.html',{'bat':bat})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def syllabus_view(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        year=request.POST['year']
        syllabus=[]
        for i in range(1,9):
            if Syllabus.objects.filter(year=year,dept=dept,sem=i).exists():
                s=Syllabus.objects.get(year=year,dept=dept,sem=i)
                syllabus.append(s)
            else:
                pass
        if bat.batch==year:
            return render(request,'hod/subject/syllabus_view.html',{'syllabus':syllabus,'year':year})
        else:
            return render(request,'hod/subject/syllabus_viewc.html',{'syllabus':syllabus,'year':year})
    else:
        syllabus=[]
        for i in range(1,9):
            if Syllabus.objects.filter(year=bat,dept=dept,sem=i).exists():
                s=Syllabus.objects.get(year=bat,dept=dept,sem=i)
                syllabus.append(s)
            else:
                pass
        return render(request,'hod/subject/syllabus_view.html',{'syllabus':syllabus,'year':bat.batch})


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def syllabus_update(request,sem):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        file=request.FILES['file']
        s=Syllabus.objects.get(year=bat,dept=dept,sem=sem)
        s.delete()
        s=Syllabus.objects.create(year=bat,dept=dept,sem=sem,file=file)
        s.save()
        syllabus=Syllabus.objects.filter(year=bat,dept=dept)
        messages.info(request,'syllabus updated succesfully')
        return render(request,'hod/subject/syllabus_view.html',{'syllabus':syllabus,'year':bat})
    return render(request,'hod/subject/syllabus_update.html',{'year':bat.batch,'dept':dept,'sem':sem})
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def syllabus_delete(request,sem):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    return render(request,'hod/subject/syllabus_delete.html',{'year':bat.batch,'dept':dept,'sem':sem})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def syllabus_delete_confirm(request,sem):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if Syllabus.objects.filter(year=bat,dept=dept,sem=sem).exists():
        s=Syllabus.objects.get(year=bat,dept=dept,sem=sem)
        s.delete()
        messages.info(request,"syllabus deleted successfully")
        return redirect("syllabus_view")
    else:
        messages.info(request,'syllabus not found')
        return redirect("syllabus_view")


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def sem_syllabus(request,sem,year):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    
    if Syllabus.objects.filter(year=year,dept=dept,sem=sem).exists():
        s=Syllabus.objects.get(year=year,dept=dept,sem=sem)
        return redirect('/media/{0}'.format(s.file))
    else:
        
        subject=[]
        for i in range(1,9):
            if Subject_sem.objects.filter(year=year,dept=dept,sem=i).exists():
                s=Subject_sem.objects.filter(year=year,dept=dept,sem=i)
                subject.append(s)
            else:
                pass

        if bat.batch==year:
            messages.info(request,'syllabus does not exists')
            return render(request,'hod/subject/subject_viewc.html',{'subject':subject})
        else:
            messages.info(request,'syllabus does not exists')
            return render(request,'hod/subject_view.html',{'subject':subject})
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def assign_ct(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        sem=request.POST['sem']
        sec=request.POST['sec']
        if Class.objects.filter(year=bat,branch=dept,sem=sem,sec=sec).exists():
            class_id=Class.objects.get(year=bat,branch=dept,sem=sem,sec=sec)
            if Subject_sem.objects.filter(year=bat,dept=dept,sem=sem).exists():
                subject1=Subject_sem.objects.filter(year=bat,sem=sem,dept=dept)
                subject2=AssignCT.objects.filter(class_id=class_id)
                subject3=[]
                subject=[]
                for i in subject2:
                    subject3.append(i.subject_id)
                for i in subject1:
                    if i not in subject3:
                        subject.append(i)
               
                if len(subject)==0:
                    messages.error(request,"No Subject found !")
                    return redirect('assign_ct')
                teacher=[]
                if Profile.objects.filter(department=dept,designation='faculty').exists():
                    tea=Profile.objects.filter(department=dept,designation='faculty')
                    for t in tea:
                        i=User.objects.get(username=t.user)
                        teacher.append(i)
    
                    return render(request,'hod/subject/assignct.html',{'class':class_id,'teacher':teacher,'subject':subject})
                
                else:
                    messages.error(request,'you have not any teacher for assign to subject')
                    return render(request,'hod/subject/assignct.html',{'bat':bat,'dept':dept})
            else:
                messages.error(request,'Subjects not found !')
                return render(request,'hod/subject/assignct.html',{'bat':bat,'dept':dept})
        else:
            messages.error(request,'class does not exists')
            return render(request,'hod/subject/assignct.html',{'bat':bat,'dept':dept})
    return render(request,'hod/subject/assignct.html',{'bat':bat,'dept':dept})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def add_assignct(request,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    class_id=Class.objects.get(year=bat,branch=dept,sem=sem,sec=sec)
    if Subject_sem.objects.filter(sem=sem,year=bat,dept=dept).exists():
       
        subject1=Subject_sem.objects.filter(year=bat,sem=sem,dept=dept)
        subject3=[]
        subject2=AssignCT.objects.filter(class_id=class_id)
        subject=[]
        for i in subject2:
            subject3.append(i.subject_id)
        for i in subject1:
            if i not in subject3:
                subject.append(i)
        for s in subject:
            t=request.POST[s.subject_code]
            if User.objects.filter(username=t).exists():
                teacher=User.objects.get(username=t)
                a=AssignCT.objects.create(class_id=class_id,subject_id=s,teacher_id=teacher)
                a.save()
            else:
                messages.info(request,' No subject found')
                return redirect('assign_ct')
        messages.info(request,"assign sucessfully")
        return redirect('assign_ct')
    else:
        messages.info(request,"assign unsucessfull")
        return render(request,'hod/subject/assignct.html',{'bat':bat,'dept':dept})        


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def class_view(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        year=request.POST['year']
        if batch.objects.filter(batch=year).exists():
            if year==bat.batch:
                class_id=Class.objects.filter(year=bat,branch=dept)
                object_list=[]
                for  c  in class_id:
                    if int(c.sem)>0:
                        a=AssignCT.objects.filter(class_id=c)
                        object_list.append(a)
                
                return render(request,'hod/class_view.html',{'object_list':object_list})

            else:
                class_id=Class.objects.filter(year=year,branch=dept)
                object_list=[]
                for  c  in class_id:
                    a=AssignCT.objects.filter(class_id=c)                             
                    object_list.append(a)
                return render(request,'hod/subject/class_viewc.html',{'object_list':object_list})
        else:
            messages.info(request,'this batch is not exists')
            return render(request,'hod/class_view.html')
    return render(request,'hod/class_view.html')

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def class_teacher_update(request,subject_code,sem,sec):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    if request.method=='POST':
        teacher=request.POST['teacher']
        teacher_id=User.objects.get(username=teacher)
        class_id=Class.objects.get(year=bat,branch=dept,sem=sem,sec=sec)
        subject_id=Subject_sem.objects.get(year=bat,sem=sem,subject_code=subject_code,dept=dept)
        AssignCT.objects.filter(class_id=class_id,subject_id=subject_id).update(teacher_id=teacher_id)
        messages.info(request,"teacher updated sucessfully")
        class_ids=Class.objects.filter(year=bat,branch=dept)
        object_list=[]
        for  c  in class_ids:
            if int(c.sem)>0:
                a=AssignCT.objects.filter(class_id=c)
                object_list.append(a)
                
        return render(request,'hod/class_view.html',{'object_list':object_list})

    else:
        if Class.objects.filter(year=bat,branch=dept,sem=sem,sec=sec).exists():
            class_id=Class.objects.get(year=bat,branch=dept,sem=sem,sec=sec)
            if Subject_sem.objects.filter(year=bat,sem=sem,subject_code=subject_code,dept=dept).exists():
                subject_id=Subject_sem.objects.get(year=bat,sem=sem,subject_code=subject_code,dept=dept)
         
                teacher=[]
                if Profile.objects.filter(department=dept,designation='faculty').exists():
                    tea=Profile.objects.filter(department=dept,designation='faculty')
                    for t in tea:
                        i=User.objects.get(username=t.user)
                        teacher.append(i)
                    return render(request,"hod/subject/class_teacher_update.html",{'class_id':class_id,'subject_id':subject_id,'teacher':teacher})

        
            
        
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')            
def department_student(request,dept):
    query=request.GET.get('query')
    sem=request.GET.get('sem','');
    sec=request.GET.get('sec','');
    batch=request.GET.get('batch','');
    if query==None:
        query=''
 
    if len(query)>100:
        messages.warning(request,"Your Query is too long ............ ")
        return render(request,'hod/student/student.html')
    if Student.objects.filter(branch=dept).exists():
        student=Student.objects.filter(branch=dept).filter(sem__icontains=sem).filter(sec__icontains=sec).filter(Q(enrollment__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return render(request,'hod/student/student.html',{'student':student})
   
    else:
        messages.error(request,'Student Not found')
        return redirect('hod_dash')
   


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def assign_tg(request):
    bat=batch.objects.latest('batch')
    dept=request.user.profile.department
    
    if request.method=='POST':
        tea=request.POST['teacher']
        sec=request.POST['sec']
        teacher_id=User.objects.get(username=tea)
        if TutorGuard.objects.filter(year=bat,sem='1',branch=dept,sec=sec).count()<2:
            if TutorGuard.objects.filter(year=bat,sem='1',branch=dept,sec=sec,teacher_id=teacher_id).exists():
                messages.error(request,'This Tutor already assign to this class')
                return redirect('assign_tg')
            else:
                a=TutorGuard.objects.create(year=bat,sem='1',branch=dept,sec=sec,teacher_id=teacher_id)
                a.save()
                messages.success(request,'TG assign to class {} {} successfully'.format(dept,sec))
                return redirect('assign_tg')
                    
        else:
            messages.error(request,' 2 Tutor Guardian already assign to this class')
            return redirect('assign_tg')

    else:
        class_tg=[]
        teacher=[]
        for b in range(int(bat.batch)-4,int(bat.batch)+1):
            if TutorGuard.objects.filter(year=b,branch=dept).exists():
                tg=TutorGuard.objects.filter(year=b,branch=dept)
                class_tg.append(tg)
        if Profile.objects.filter(department=dept,designation='faculty').exists():
            tea=Profile.objects.filter(department=dept,designation='faculty')
            for t in tea:
                i=User.objects.get(username=t.user)
                teacher.append(i)
            return render(request,'hod/class/assigntg.html',{'bat':bat,'dept':dept,'teacher':teacher,'class_tg':class_tg})
                
        else:
            messages.error(request,'you have not any teacher for assign to class')
            return render(request,'hod/class/assigntg.html',{'bat':bat,'dept':dept,'class_tg':class_tg})
       
@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def update_tg(request):
    dept=request.user.profile.department

    teacher=[]
        
    if request.method=='POST':
        teachers=request.POST['teacher']
        sec=request.POST['sec']
        sem=request.POST['sem']
        year=request.POST['batch']
        teacher_id=User.objects.get(username=teachers)
        
        if Profile.objects.filter(department=dept,designation='faculty').exists():
            tea=Profile.objects.filter(department=dept,designation='faculty')
            for t in tea:
                i=User.objects.get(username=t.user)
                teacher.append(i)
            return render(request,'hod/class/tg_update.html',{'batch':year,'sem':sem,'sec':sec,'tea':teacher_id,'teacher':teacher})

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def tg_updated(request):
    dept=request.user.profile.department

    teacher=[]
    if request.method=='POST':
        teachers=request.POST['teacher']
        teacher1=request.POST['teachers']
        sec=request.POST['sec']
        sem=request.POST['sem']
        year=request.POST['batch']
        teacher_id1=User.objects.get(username=teacher1)
        teacher_id=User.objects.get(username=teachers)
        if TutorGuard.objects.filter(year=year,branch=dept,sem=sem,sec=sec,teacher_id=teacher_id1).exists():
            t=TutorGuard.objects.filter(year=year,branch=dept,sem=sem,sec=sec,teacher_id=teacher_id1).update(teacher_id=teacher_id)
            messages.success(request,'updated successfully ')
            return redirect('assign_tg')
    else:
        return redirect('assign_tg')



