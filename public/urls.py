from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    #about
    url(r'^about/$', views.about, name="about"),
    #konser
    url(r'^konser/$', views.konser, name="konser"),
    #contact
    url(r'^contact-us/$', views.contact, name="contact"),
    #/article_detail
    url(r'^event/(?P<article_id>[0-9]+)/$', views.article_detail, name='article_detail'),
    #/event_detail
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    #/event_new
    url(r'^event/new/$', views.event_new, name='event_new'),
    #/register
    url(r'^register/$', views.register, name='register'),
]
