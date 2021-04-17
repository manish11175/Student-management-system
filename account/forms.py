from django import forms
from django.contrib.auth.models	import	User
from.models	import	Profile,StudentProfile,AdminProfile
class UserEditForm(forms.ModelForm):				
    class Meta:								
        model=User
        fields=('first_name','last_name','email')
        widgets={
                'email':forms.EmailInput(attrs={'class':'form-control'}),
                'first_name':forms.TextInput(attrs={'class':'form-control'}),
                'last_name':forms.TextInput(attrs={'class':'form-control'}),}
class ProfileEditForm(forms.ModelForm):				
    class Meta:								
        model	=	Profile								
        fields	=	('date_of_birth','photo','contact_no','country','state','District','city_town_area','pincode')
        widgets={
                'date_of_birth':forms.DateInput(attrs={'class':'form-control'}),
                'photo':forms.FileInput(attrs={'class':'form-control'}),
                'contact_no':forms.NumberInput(attrs={'class':'form-control'}),
                'country':forms.TextInput(attrs={'class':'form-control'}),
                'state':forms.TextInput(attrs={'class':'form-control'}),
                'District':forms.TextInput(attrs={'class':'form-control'}),
                'city_town_area':forms.TextInput(attrs={'class':'form-control'}),
                'pincode':forms.NumberInput(attrs={'class':'form-control'}),}
class StudentProfileEditForm(forms.ModelForm):				
    class Meta:								
        model	=	StudentProfile								
        fields	=	('date_of_birth','photo','contact_no') 
        widgets={
                'date_of_birth':forms.DateInput(attrs={'class':'form-control'}),
                'photo':forms.FileInput(attrs={'class':'form-control'}),
                'contact_no':forms.NumberInput(attrs={'class':'form-control'}),}       
   
class AdminProfileEditForm(forms.ModelForm):				
    class Meta:								
        model	=	AdminProfile								
        fields	=	('date_of_birth','photo','contact_no','country','state','District','city_town_area','pincode') 
        widgets={
                'date_of_birth':forms.DateInput(attrs={'class':'form-control'}),
                'photo':forms.FileInput(attrs={'class':'form-control'}),
                'contact_no':forms.NumberInput(attrs={'class':'form-control'}),
                'country':forms.TextInput(attrs={'class':'form-control'}),
                'state':forms.TextInput(attrs={'class':'form-control'}),
                'District':forms.TextInput(attrs={'class':'form-control'}),
                'city_town_area':forms.TextInput(attrs={'class':'form-control'}),
                'pincode':forms.NumberInput(attrs={'class':'form-control'}),}       
 
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input'}))				
    password2=forms.CharField(label='Repeat	password',widget=forms.PasswordInput(attrs={'class':'input'}))

    class Meta:

        model=User								
        fields=('username','first_name','last_name','email')
        
    def	clean_password2(self):							
        cd=self.cleaned_data								
        if	cd['password']!=cd['password2']:												
            raise	forms.ValidationError('Passwords	don\'t	match.')								
        return	cd['password2']

class StudentRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input'}))				
    password2=forms.CharField(label='Repeat	password',widget=forms.PasswordInput(attrs={'class':'input'}))

    class Meta:

        model=User								
        fields=('username','first_name','last_name','email')
        
    def	clean_password2(self):							
        cd=self.cleaned_data								
        if	cd['password']!=cd['password2']:												
            raise	forms.ValidationError('Passwords	don\'t	match.')								
        return	cd['password2']


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)