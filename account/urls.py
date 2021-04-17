from.import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path,include



urlpatterns=[
			#path('login/',	views.user_login,	name='login'),
            path('teacherlogin/',views.teacher_login,name='teacher_login'),
            path('teacherlogout/',views.teacher_logout,name='teacher_logout'),
            path('studentlogout/',views.student_logout,name='student_logout'),
            path('hodlogout/',views.hod_logout,name='hod_logout'),
            path('adminlogout/',views.admin_logout,name='admin_logout'),
            path('student_edit/',views.student_edit,name="student_edit"),
            path('student_password_change/',views.StudentPasswordChange,name='student_password_change'), 
            path('hodlogin/',views.hod_login,name="hod_login"),
            path('adminlogin/',views.admin_login,name='admin_login'),
          
            path('student_login/',views.student_login,name='student_login'), 
            path('register/',views.register,name='register'),
            path('studentregister/',views.StudentRegister,	name='student_register'),
            path('password_change/',views.PasswordChange,name='password_change'), 
            path('hod_password_change/',views.HodPasswordChange,name='hod_pass_change'), 
            path('admin_password_change/',views.AdminPasswordChange,name='admin_pass_change'), 
            path('password_reset/',	auth_views.PasswordResetView.as_view(),name='password_reset'),
            path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
            path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
            path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
            path('edit/',views.edit,name='edit'),
            path('hodedit/',views.hodedit,name='hod_edit'),
            path('adminedit/',views.adminedit,name='admin_edit'),


            

]