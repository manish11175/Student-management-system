from django.urls import	path
from.import	views
from django.conf.urls import url
from user.views import *

from django.contrib.auth	import	views   as	auth_views


urlpatterns	=[				
    path('admindash/',views.admin_dash,name='admin_dash'),
    path('adminprofile/',views.admin_profile,name='admin_profile'),
    path('collegehod/',views.college_hod,name="college_hod"),
    path('start-new-batch/',views.StartNewBatch,name="start_new_batch"),
    path('web-settings/',views.web_settings,name="web_settings"),
    path('footer-link/',views.footer_link,name="footer_link"),
    path('carausal/',views.carausal,name="carausal"),
    ]