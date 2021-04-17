
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Student,StuAdmission,StuBank,Family,StuLocalGuard,StudentEducation,\
                StuHostel,StuMedical,Stu_placement,\
                StudentResult,StudentMidsem,StudentFee,StudentAddress,StudentResident,Tgcalling,AttendanceMessages

from.models import batch,Attendance,TotalAttendance

@admin.register(StudentEducation)
class StudentEducationAdmin(admin.ModelAdmin):
    list_display=('enrollment','course','roll_no','board','year_of_passing','total_mark','obtain_mark','percent')
  
@admin.register(Tgcalling)
class TgcallingAdmin(admin.ModelAdmin):
    list_display=('enrollment','sem','date','contact_no','contact_person','reason','description','faculty')
  
    
@admin.register(TotalAttendance)
class TotalAttendanceAdmin(admin.ModelAdmin):
    list_display=('enrollment','sem','att_class','total_class','attendance','classes_to_attend')
    
@admin.register(StudentResident)
class StudentResidentAdmin(admin.ModelAdmin):
    list_display=('enrollment','house_no','street','state','country','pincode')
    
@admin.register(StudentAddress)
class StudentAddressAdmin(admin.ModelAdmin):
    list_display=('enrollment','house_no','street','state','country','pincode')
    

@admin.register(StudentMidsem)
class StudentMidsemAdmin(admin.ModelAdmin):
    list_display=('enrollment','sem','total_mark','obtain_mark','avg')
    
@admin.register(Attendance)
class Attendance(admin.ModelAdmin):
    list_display=('enrollment','sem','date','attend')
    list_filter	=	('enrollment','sem','date')
   
    class Meta:
        ordering = ['-enrollment']



@admin.register(StudentFee)
class StudentFee(admin.ModelAdmin):
    list_display=('enrollment','sem','total_amt','amt_due','amt_paid','receipt_no','date')

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display	=	('enrollment',	'sem','sgpa','cgpa')
    list_filter	=	('enrollment','sem')
    

@admin.register(batch)
class batchAdmin(admin.ModelAdmin):
    pass
  

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display	=	('enrollment',	'first_name','last_name','Email','owner','batch','branch','sem','sec')
    list_filter	=	('owner','batch','phone')
    search_fields	=	('enrollment','batch')
    class Meta:
        ordering = ['-enrollment']


@admin.register(StuAdmission)
class StuAdmissionAdmin(admin.ModelAdmin):
    list_display	=	('enrollment',	'branch',	'entrance',	'sec')
    list_filter	=	('enrollment','branch','sem')
    search_fields	=	('enrollment',	'branch')

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display=('enrollment','father_name','father_mob','mother_name','mother_mob')
    list_filter	=('enrollment','father_name','mother_name')
    search_fields=('enrollment','father_name','mother_name')



@admin.register(StuLocalGuard)
class StuLocalGuardAdmin(admin.ModelAdmin):
    list_display=('enrollment','local_guard_name',	'guard_mob','guard_address')
    list_filter=('enrollment','local_guard_name')
    search_fields=('enrollment','local_guard_name')


@admin.register(StuHostel)
class StuHostelAdmin(admin.ModelAdmin):
    list_display	=	('enrollment','name_hostel','room_no')
    list_filter	=	('enrollment','name_hostel','room_no')
    search_fields	=	('enrollment',	'name_hostel')


@admin.register(StuMedical)
class StuMedicalAdmin(admin.ModelAdmin):
    list_display	=	('enrollment','blood_group','physical_disable')
    list_filter	=	('enrollment','blood_group')
    search_fields	=	('enrollment',	'blood_group')

@admin.register(StuBank)
class StuBankAdmin(admin.ModelAdmin):
    list_display	=	('enrollment','bank_name',	'bank_ac','bank_ifsc','bank_branch')
    list_filter	=	('enrollment','bank_ac','bank_branch','bank_name')
    search_fields	=	('enrollment',	'bank_ac','bank_name')


@admin.register(Stu_placement)
class Stu_placementAdmin(admin.ModelAdmin):
    list_display =	('enrollment','placement_date',	'company_name','placement_result','join_date','placement_package')
    list_filter	=	('enrollment','placement_result','placement_package')
    search_fields	=	('enrollment',	'placement_result')
@admin.register(AttendanceMessages)
class AttendanceMessagesAdmin(admin.ModelAdmin):
    list_display=('message_type','messages')


