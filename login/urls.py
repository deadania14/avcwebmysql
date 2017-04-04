from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    #/restricted views
    url(r'^restricted/$', views.restricted, name='restricted'),
    #/logout
    url(r'^logout/$', views.user_logout, name='logout'),
]
