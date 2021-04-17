from django.db import models
from django.contrib.auth.models import User 
from account.models import Profile
from django.conf import settings
from django.contrib.auth.models import UserManager
import math
Course_Choice	=	(('x',	'x'),('xii',	'xii'),('diploma',	'diploma'),('jee',	'jee'),('gate',	'gate'),('ug',	'ug'),('pg',	'pg'),
    					('other',	'other'))
GENDER_CHOICES	=	(('male',	'MALE'),
    					('female',	'FEMALE'))
BRANCH_CHOICES	=	(('cs',	'CS'),
    					('it',	'IT'),
                        ('ce',	'CE'),
                        ('me',	'ME'),
                        ('ec',	'EC'),
                        ('ee',	'EE'),)

Messages=(('suspension','suspension'),
          ('attendance','attendance'),('warning','warning'))
SEC_CHOICES=(('A','A'),('B','B'),('C','C'))
Attend=((1,'present'),(0,'absent'),(0.5,'half_day'))
SEM_CHOICES=(('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'))
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
class batch(models.Model):
    batch=models.CharField(primary_key=True,max_length=4)
    
    def __str__(self):
        return self.batch
class Student(models.Model):
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_created")
    enrollment=models.CharField(max_length=20,primary_key=True,unique=True)
    first_name=models.CharField(max_length=50,blank=False,default="")
    last_name=models.CharField(max_length=50,blank=False,default="")
    Email=models.EmailField(max_length=50 , blank=False,default="")
    phone=models.CharField(max_length=10,blank=False,default="")
    photo=models.FileField(upload_to="student/%Y/%m/%d/",default="")
    dob=models.DateField(default="",blank=True,null=True)
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES,default='male')
    batch=models.ForeignKey(batch,on_delete=models.CASCADE)
    branch=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    sec=models.CharField(max_length=2,choices=SEC_CHOICES,default='A')
    active=models.BooleanField(default=True)
    @property
    def lifespan(self):
        return '%s - present' % self.dob.strftime('%d/%m/%Y')
    
    def __str__(self):
        return self.enrollment

class StudentEducation(models.Model):
    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_education')
    course=models.CharField(max_length=50,default="tenth",choices=Course_Choice)
    roll_no=models.CharField(max_length=50,default="")
    rank=models.IntegerField(default="")
    board=models.CharField(max_length=50,default="")
    year_of_passing=models.IntegerField(default="")
    total_mark=models.FloatField(default="")
    obtain_mark=models.FloatField(default="")
    percent=models.FloatField(default="")
    marksheet=models.FileField(upload_to="student/marksheet/%Y/",default="")
    class Meta:
        unique_together = (('enrollment', 'course'))
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)

class Tgcalling(models.Model):
    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='tg_calling')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    date=models.DateField(default="")
    contact_no=models.CharField(max_length=10,blank=False,default="")
    contact_person=models.CharField(max_length=50,default="")
    reason=models.CharField(max_length=100,default="")
    description=models.CharField(max_length=500,default="")
    faculty=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('enrollment', 'date'))
    
class Attendance(models.Model):
   
    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='stu_attendance')
    sem=models.CharField(max_length=5,choices=SEM_CHOICES,default='I')
    date=models.DateField(default="")
    week=models.IntegerField(default=0)
    attend=models.FloatField(default=0,max_length=5,choices=Attend)
    class Meta:
        unique_together = (('enrollment', 'date'),)
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)

  

class TotalAttendance(models.Model):
    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='total_attendance')
    sem=models.CharField(max_length=6,choices=SEM_CHOICES,default='I')
    class Meta:
        unique_together = (('enrollment', 'sem'))
   

    @property
    def att_class(self):
        enroll = Student.objects.get(enrollment=self.enrollment)
        sem=enroll.sem
        att_class = Attendance.objects.filter( enrollment=enroll,sem=sem, attend=1).count()
        return att_class

    @property
    def total_class(self):
        enroll = Student.objects.get(enrollment=self.enrollment)
        sem=enroll.sem
        total_class = Attendance.objects.filter(enrollment=enroll,sem=sem).count()
        return total_class

    @property
    def attendance(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        sem=enroll.sem
        total_class = Attendance.objects.filter(enrollment=enroll,sem=sem).count()
        att_class = Attendance.objects.filter(enrollment=enroll, sem=sem, attend=1).count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance

    @property
    def classes_to_attend(self):
        
        enroll= Student.objects.get(enrollment=self.enrollment)
        sem=enroll.sem
        total_class = Attendance.objects.filter(enrollment=enroll,sem=sem).count()
        att_class = Attendance.objects.filter(enrollment=enroll,sem=sem, attend=1).count()
        cta = math.ceil((0.75*total_class - att_class)/0.25)
        if cta < 0:
            return 0
        return cta

    
    
class StudentResident(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_resident')
    house_no=models.CharField(max_length=50,default="")
    street=models.CharField(max_length=50,default="")
    city=models.CharField(max_length=50,default="")
    district=models.CharField(max_length=50,default="")
    state=models.CharField(max_length=50,default="Madhya Pradesh",choices=state_choices)
    country=models.CharField(max_length=5,default='india')
    pincode=models.CharField(max_length=6,default='')
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)

class StudentAddress(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_address')
    house_no=models.CharField(max_length=50,default="")
    street=models.CharField(max_length=50,default="")
    city=models.CharField(max_length=50,default="")
    district=models.CharField(max_length=50,default="")
    state=models.CharField(max_length=50,default="Madhya Pradesh",choices=state_choices)
    country=models.CharField(max_length=5,default='india')
    pincode=models.CharField(max_length=6,default='')
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)
class StudentResult(models.Model):
    Result=(('fail','Fail'),
    		('pass','Pass'))
    SEM_CHOICES=(('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'),)

    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='result_detail')
    sem=models.CharField(max_length=5,choices=SEM_CHOICES,default='I')
    result=models.CharField(max_length=4,choices=Result,default='fail')
    sgpa=models.FloatField(default="")
    cgpa=models.FloatField(default="")
    if_fail=models.CharField(max_length=100,default="")
    marksheet=models.FileField(upload_to="result/%Y/%m/%d/",default="")
    class Meta:
        unique_together = (('enrollment', 'sem'))
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        return '%s' % (enroll.enrollment)
   
class StudentFee(models.Model):
    SEM_CHOICES=(('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'),)

    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='fee_detail')
    sem=models.CharField(max_length=5,choices=SEM_CHOICES,default='I')
    total_amt=models.FloatField(default="")
    amt_due=models.FloatField(default="")
    amt_paid=models.FloatField(default="")
    receipt_no=models.CharField(max_length=100,default="")
    date=models.DateField(default="")
    receipt=models.FileField(upload_to="fee/%Y/%m/%d/",default="")
    class Meta:
        unique_together = (('enrollment', 'receipt_no'))
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)

class StudentMidsem(models.Model):
    MidTerm=(('1','1'),
    		('2','2'))
    SEM_CHOICES=(('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'),)

    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='result_midsem')
    sem=models.CharField(max_length=5,choices=SEM_CHOICES,default='I')
    
    midterm=models.CharField(max_length=4,choices=MidTerm,default='1')
    total_mark=models.FloatField(default="")
    obtain_mark=models.FloatField(default="")
    avg=models.FloatField(default="")
    class Meta:
        unique_together = (('enrollment', 'sem','midterm'))
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)
    
   
 
class StuAdmission(models.Model):
    BRANCH_CHOICES	=	(('cs',	'CS'),
    					('it',	'IT'),
                        ('ce',	'CE'),
                        ('me',	'ME'),
                        ('ec',	'EC'),
                        ('ee',	'EE'),)
    SEM_CHOICES=(('I','1'),('II','2'),('III','3'),('IV','4'),('V','5'),('VI','6'),('VII','7'),('VII','8'),)
    SEC_CHOICES=(('A','A'),('B','B'),('C','C'))
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_detail')
    entrance=models.CharField(max_length=50,default="")
    admisbase=models.CharField(max_length=50,default="")
    sch_no=models.CharField(max_length=50,default="")
    branch=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=5,choices=SEM_CHOICES,default='I')
    sec=models.CharField(max_length=2,choices=SEC_CHOICES,default='A')
    year=models.IntegerField(default="")
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)
  



class Family(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_family')
    father_name=models.CharField(max_length=50,default="")
    father_mob=models.CharField(max_length=50,default="")
    father_email=models.EmailField(max_length=50,default="")
    father_organi=models.CharField(max_length=50,default="")
    father_occup=models.CharField(max_length=50,default="")
    father_income=models.IntegerField(default="")
    father_office=models.CharField(max_length=50,default="")
    mother_name=models.CharField(max_length=50,default="")
    mother_mob=models.CharField(max_length=50,default="")
    mother_email=models.EmailField(max_length=50,default="")
    mother_organi=models.CharField(max_length=50,default="")
    mother_occup=models.CharField(max_length=50,default="")
    mother_income=models.IntegerField(default="")
    mother_office=models.CharField(max_length=50,default="")
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)
	



class StuLocalGuard(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_local_guard')
    local_guard_name=models.CharField(max_length=50,default="")
    guard_mob=models.CharField(max_length=50,default="")
    guard_address=models.CharField(max_length=50,default="")
    stu_rela_guard=models.CharField(max_length=50,default="")
   

class StuHostel(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_hostel')
    name_hostel=models.CharField(max_length=50,default="")
    room_no=models.CharField(max_length=50,default="")
    resi_address=models.CharField(max_length=50,default="")
    pincode=models.CharField(max_length=50,default="")
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)


class StuMedical(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student_medical')
    blood_group=models.CharField(max_length=50,default="")
    physical_disable=models.CharField(max_length=50,default="")
    other_med=models.CharField(max_length=50,default="")
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)
class StuBank(models.Model):
    enrollment=models.OneToOneField(Student,on_delete=models.CASCADE,related_name="student_bank_detail")
    bank_name=models.CharField(max_length=50,default="")
    bank_branch=models.CharField(max_length=50,default="")
    bank_ac=models.CharField(max_length=50,default="")
    bank_ifsc=models.CharField(max_length=50,default="")
    ac_hold_name=models.CharField(max_length=50,default="")
    aadhar_no=models.CharField(max_length=50,default="")
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)


class Stu_placement(models.Model):
    enrollment=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_placement')
    tnp_date=models.DateField(default='')
    placement_date=models.DateField(default='')
    company_name=models.CharField(default='', max_length=50)
    placement_result=models.CharField(default='', max_length=50)
    join_date=models.DateField(default='')
    placement_package=models.FloatField(default='')
    placement_remark=models.CharField(default='', max_length=50)
    def __str__(self):
        enroll= Student.objects.get(enrollment=self.enrollment)
        
        return '%s' % (enroll.enrollment)


class AttendanceMessages(models.Model):
    message_type=models.CharField(max_length=30,choices=Messages,primary_key=True,default="suspension")
    messages=models.CharField(max_length=200,blank=False)

 
       
