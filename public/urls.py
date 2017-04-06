from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    #about
    url(r'^about/$', views.about, name="about"),
    #/registration
    url(r'^registration/$', views.registration, name="registration"),
    #/event_detail
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    #/event_new
    url(r'^event/new/$', views.event_new, name='event_new'),
    #/register
    url(r'^register/$', views.register, name='register'),
]
