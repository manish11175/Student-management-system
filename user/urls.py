from django.urls import	path
from.import	views
from django.conf.urls import url
from user.views import *

from django.contrib.auth	import	views   as	auth_views


urlpatterns	=[				
    path('studentdash/',views.student_dash,name='student_dash'),
    path('student-profile/',views.student_profile,name="student_profile"),
    path('family/',views.family,name='family_update'),
    path('lg/',views.lg,name='lg_update'),
    path('medical/',views.medical,name='medical_update'),
    path('bank/',views.bank,name='bank_update'),
    path('education/',views.student_education,name="education"),
    path('hostel/',views.hostel,name='hostel_update'),
    path('admission/',views.admission,name='admission_update'),
    path('placement/',views.placement,name='placement_update'),
    path('result/',views.result,name='result_update'),
    path('midterm/',views.midterm,name='midterm_update'),
    path('fee/',views.fee,name='fee_update'),
    path('address/',views.address,name='address_update'),
    path('resident/',views.resident,name='resident_update'),
    path('residentupdate/',views.resident_update,name='resident_updates'),
    path('student_sem_attendance/',views.student_sem_attendance,name='student_sem_attendance'),
    path('student_tgcall/',views.student_tgcall,name="student_tgcall"),
    path('student_subject_attendance/',views.student_subject_attendance,name='student_subject_attendance'),
    path('student_subject/',views.student_subject,name="student_subject"),
    path('<year>/<sem>/<subject_code>/student_unit_mark/',views.student_unit_mark,name="student_unit_mark"),
    path('<year>/<sem>/<subject_code>/student_midterm_mark/',views.student_midterm_mark,name="student_midterm_mark"),
    path('<year>/<sem>/<subject_code>/student_practical_mark/',views.student_practical_mark,name="student_practical_mark"),
    path('<year>/<sem>/<subject_code>/student_project_mark/',views.student_project_mark,name="student_project_mark"),



    ]