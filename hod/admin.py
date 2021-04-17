from django.contrib import admin
from .models import Class,Subject_sem,Syllabus,AssignCT,TeacherSubjectAttendance,TeacherSubjectMark,\
    TeacherSubjectMidTerm,TeacherPracticalMark,TeacherProjectMark,TutorGuard

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display=('year','branch','sem','sec')

@admin.register(Subject_sem)
class Subject_semAdmin(admin.ModelAdmin):
    list_display=('year','dept','sem','subject_name','subject_code','subject_type')
  
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display=('year','dept','sem','file')
 
@admin.register(AssignCT)
class AssignCTAdmin(admin.ModelAdmin):
    list_display=('class_id','subject_id','teacher_id')
@admin.register(TeacherSubjectAttendance)
class TeacherSubjectAttendanceAdmin(admin.ModelAdmin):
    list_display=('student_id','subject_id','date','attend')

@admin.register(TeacherSubjectMark)
class TeacherSubjectMarkAdmin(admin.ModelAdmin):
    list_display=('student_id','subject_id','exam_type','exam_no','unit_no','total_mark','obtain_mark')
@admin.register(TeacherSubjectMidTerm)
class TeacherSubjectMidTermAdmin(admin.ModelAdmin):
    list_display=('student_id','subject_id','exam_no','total_mark','obtain_mark')

@admin.register(TeacherPracticalMark)
class TeacherPracticalMarkAdmin(admin.ModelAdmin):
    list_display=('student_id','subject_id','practical_no','total_mark','obtain_mark')

@admin.register(TeacherProjectMark)
class TeacherProjectMarkAdmin(admin.ModelAdmin):
    list_display=('student_id','subject_id','total_mark','obtain_mark')

@admin.register(TutorGuard)
class TutorGuardAdmin(admin.ModelAdmin):
    list_display=('year','teacher_id','branch','sem','sec')