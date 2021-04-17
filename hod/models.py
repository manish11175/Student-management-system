from django.db import models
from student.models import batch,Student
from account.models import Profile
from django.contrib.auth.models import User
Attend=((1,'present'),(0,'absent'),(0.5,'half_day'))
BRANCH_CHOICES	=	(('cs',	'CS'),
    					('it',	'IT'),
                        ('ce',	'CE'),
                        ('me',	'ME'),
                        ('ec',	'EC'),
                        ('ee',	'EE'),)
SEC_CHOICES=(('A','A'),('B','B'),('C','C'),('D','D'))
SEM_CHOICES=(('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'))
Subject_type=(('theory','Theory'),('practical','Practical'),('minor project','Minor Project'),('major project',"Major Project"))
Exam=(('tutorial','tutorial'),('test','test'))

Exam_no=((1,1),(2,2))
class Class(models.Model):
    year=models.ForeignKey(batch,on_delete=models.CASCADE)
    branch=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    sec=models.CharField(max_length=2,choices=SEC_CHOICES,default='A')
    
    class Meta:
        unique_together=(('year','branch','sem','sec'))
    def __str__(self):
        b= batch.objects.get(batch=self.year)
        
        return '%s' % (b.batch)+ self.branch.upper() + self.sem +self.sec


class Subject_sem(models.Model):
    year=models.ForeignKey(batch,on_delete=models.CASCADE)
    dept=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    subject_name=models.CharField(max_length=100,default='', null=False)
    subject_code=models.CharField(max_length=20,default='',null=False)
    subject_type=models.CharField(max_length=30,default="theory",choices=Subject_type)
    class Meta:
        unique_together=(('year','dept','sem','subject_code'))
    def __str__(self):
        b= batch.objects.get(batch=self.year)
        
        return '%s' % (b.batch)+ self.dept.upper() + self.sem +self.subject_code
    

class Syllabus(models.Model):
    year=models.ForeignKey(batch,on_delete=models.CASCADE)
    dept=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    file=models.FileField(upload_to="syllabus/%Y")
    class Meta:
        unique_together=(('year','dept','sem'))
    def __str__(self):
        b= batch.objects.get(batch=self.year)
        
        return '%s' % (b.batch)+ self.dept.upper() + self.sem 
    
class AssignCT(models.Model):
    class_id=models.ForeignKey(Class,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    teacher_id=models.ForeignKey(User,on_delete=models.CASCADE)    
    class Meta:
        unique_together=('class_id','subject_id')


class TeacherSubjectAttendance(models.Model):
       
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    date=models.DateField(default="")
    attend=models.FloatField(default=0,max_length=5,choices=Attend)
    class Meta:
        unique_together = (('student_id','subject_id', 'date'),)

class TeacherSubjectMark(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    exam_type=models.CharField(max_length=20,default='tutorial',choices=Exam)
    exam_no=models.IntegerField(choices=Exam_no,default=0)
    unit_no=models.IntegerField()
    total_mark=models.FloatField()
    obtain_mark=models.FloatField()
    class Meta:
        unique_together = (('student_id','subject_id', 'exam_type','exam_no','unit_no'))

class TeacherSubjectMidTerm(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    exam_no=models.IntegerField(choices=Exam_no,default=0)
    total_mark=models.FloatField()
    obtain_mark=models.FloatField()
    class Meta:
        unique_together = (('student_id','subject_id', 'exam_no'))

class TeacherPracticalMark(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    practical_no=models.IntegerField(choices=Exam_no,default=0)
    total_mark=models.FloatField()
    obtain_mark=models.FloatField()
    class Meta:
        unique_together = (('student_id','subject_id', 'practical_no'))
class TeacherProjectMark(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject_sem,on_delete=models.CASCADE)
    total_mark=models.FloatField()
    obtain_mark=models.FloatField()
    class Meta:
        unique_together = (('student_id','subject_id'))

class TutorGuard(models.Model):
    teacher_id=models.ForeignKey(User,on_delete=models.CASCADE) 
    year=models.ForeignKey(batch,on_delete=models.CASCADE,default='2017')
    branch=models.CharField(max_length=10,choices=BRANCH_CHOICES,default='cs')
    sem=models.CharField(max_length=2,default='I',choices=SEM_CHOICES)
    sec=models.CharField(max_length=2,choices=SEC_CHOICES,default='A')
    class Meta:
        unique_together = (('year','teacher_id','sem','branch','sec'))