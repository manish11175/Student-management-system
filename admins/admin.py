from.models import Footer,Carausal
from django.contrib import admin

@admin.register(Footer)
class FooterDownloadAdmin(admin.ModelAdmin):
    list_display=('link_name','link')

@admin.register(Carausal)
class CarausalAdmin(admin.ModelAdmin):
    list_display=['slide_no','image','title','description']