from django.conf.urls import url
from PerfectCRM.Perfectcrm.video import views

urlpatterns = [
    url(r'^video-(?P<level_id>\d+)-(?P<category_id>\d+).html',views.video,name='table_video'),
    url(r'^video2-(?P<dr_id>\d+)-(?P<level_id>\d+)-(?P<category_id>\d+).html',views.video2,name='table_video2'),
]