from django.db import models

Footer_link=(('download','download'),('quick_link','quick_link'),('suggest_link','suggest_link'),('sister_concern','sister_concern'))

Social_Media=(('facebook','facebook'),('instagram','instagram'),('google','google'),('linkdin','linkdin'),('twitter','twitter'),('wiki','wiki')\
    ,('youtube','youtube'),('pinterest','pinterest'),('tumblr','tumblr'))
class Footer(models.Model):
    link_cate=models.CharField(max_length=50,choices=Footer_link)
    link_name=models.CharField(max_length=50)
    link=models.CharField(max_length=150,default='#')
    class Meta:
        unique_together=('link_cate','link_name')


class Carausal(models.Model):
    slide_no=models.IntegerField(primary_key=True)
    image=models.ImageField(upload_to='admin/website/carausal/')
    title=models.CharField(default='',max_length=50)
    description=models.CharField(default='',max_length=150)