from django	import	forms

from django.forms.models import	inlineformset_factory 
from.models import	Student,StuMedical,Stu_placement
from.models import  StuBank,StuHostel,StudentFee
from.models	import	Student,StuAdmission,Family,StuLocalGuard,StuMedical,StudentAddress,StudentResident
from student.models import batch

        



from .models import Student
from django import forms
class StudentSearchForm(forms.Form):
    search_text= forms.CharField(
                    required = False,
                    label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Search name or enrollment!'})
                  )

    