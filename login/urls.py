from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    #/restricted views
    url(r'^restricted/$', views.restricted, name='restricted'),
    #/logout
    url(r'^logout/$', views.user_logout, name='logout'),
    #change_password
    url(r'^change_password/$', views.change_password, name='change_password'),
    #/forgot-password
    #url(r'^forgot-password/$', views.user_forgot_password, name='fopassword'),


]
