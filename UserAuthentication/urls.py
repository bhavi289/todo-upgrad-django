from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'UserAuthentication'

urlpatterns = [
    url(r'^sign-up/$', views.SignUp, name='SignUp'),
    url(r'^login/$', views.Login, name='Login'),
    url(r'^logout/$', logout, {'next_page': '/user-authentication/login'}, name='logout'),
]