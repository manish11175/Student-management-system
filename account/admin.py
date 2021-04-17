from django.contrib import admin
from django.contrib.auth.models import User,auth
from django.contrib	import admin 
from.models	import	Profile,StudentProfile,AdminProfile
from django.contrib.auth.models import User, Group

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):				
    list_display=['user','date_of_birth','photo','contact_no','department','role','activate','join_date']
    
    
    class Meta:
        ordering = ['-user']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):				
    list_display=['user','date_of_birth','photo','contact_no','department','designation','activate','join_date']
    list_filter	=('department','designation','activate')
    search_fields=('department','designation')
    
    class Meta:
        ordering = ['-user']
@admin.register(StudentProfile)
class ProfileAdmin(admin.ModelAdmin):				
    list_display=['user','date_of_birth','photo','contact_no','department','batch','sec','role','activate']
    list_filter	=	('department','batch','activate')
    search_fields	=	('user','batch','department')
    class Meta:
        ordering = ['-user']

