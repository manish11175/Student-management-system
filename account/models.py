
from django.db import models 
from django.conf import settings
SEC_CHOICES=(('A','A'),('B','B'),('C','C'))	

BRANCH_CHOICES	=	(('cs',	'CS'),
    					('it',	'IT'),
                        ('ce',	'CE'),
                        ('me',	'ME'),
                        ('ec',	'EC'),
                        ('ee',	'EE'),)
role	=	(('hod','Hod'),('hod1','Hod1'),('faculty',	'Faculty'))
   
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
                     ("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),
                     ("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),
                     ("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
                     ("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),
                     ("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),
                     ("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),
                     ("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),
                     ("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
                     ("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),
                     ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
                     ("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
                     ("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),
                     ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
                     ("Puducherry","Puducherry"))
class AdminProfile(models.Model):				
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True,	null=True)
    contact_no=models.CharField(max_length=10,blank=False,default="")
    department=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    role=models.CharField(max_length=30,default="admin")	
    photo=models.ImageField(upload_to='admin/%Y/%m/%d/',blank=True)
    country =models.CharField(max_length=30,default="India")
    state=models.CharField(max_length=50,default="Madhya Pradesh",choices=state_choices)
    District=models.CharField(max_length=50,default="")
    city_town_area=models.CharField(max_length=50,default="")
    pincode=models.CharField(max_length=50,default="")
    join_date=models.DateTimeField(auto_now=True)
    activate=models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Profile(models.Model):				
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True,	null=True)
    contact_no=models.CharField(max_length=10,blank=False,default="")
    department=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    designation=models.CharField(max_length=30,choices=role,default="faculty")				
    photo=models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    country =models.CharField(max_length=30,default="India")
    state=models.CharField(max_length=50,default="Madhya Pradesh",choices=state_choices)
    District=models.CharField(max_length=50,default="")
    city_town_area=models.CharField(max_length=50,default="")
    pincode=models.CharField(max_length=50,default="")
    activate=models.BooleanField(default=False)
    join_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
	
class StudentProfile(models.Model):				
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True,	null=True)
    contact_no=models.CharField(max_length=10,blank=False,default="")
    department=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    role=models.CharField(max_length=30,default="student")	
    batch=models.IntegerField(default='')
    sec=models.CharField(max_length=2,choices=SEC_CHOICES,default='A')
   	
    photo=models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    activate=models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
	