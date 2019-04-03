from django.conf.urls import url, include
from . import views

app_name = 'Schedule'

urlpatterns = [
    url(r'^home/$', views.Home, name='Home'),
    url(r'^add-schedule/$', views.AddSchedule, name='AddSchedule'),
    url(r'^add-tasks/$', views.AllTasks, name='AllTasks'),

    # url(r'^check_reminder/$', views.check_reminder, name='check_reminder'),
    # url(r'^edit-schedule/$', views.EditSchedule, name='EditSchedule'),
]