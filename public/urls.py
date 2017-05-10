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
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article_detail, name='article_detail'),
    #/event_detail
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    #/event_new
    url(r'^event/$', views.events, name='events'),
    #/register
    url(r'^register/$', views.register, name='register'),
    #/myprofile
    url(r'^profile/$', views.myprofile, name="myprofile"),
    #/edit profile
    url(r'^update_profile/(?P<pk>[\-\w]+)/$', views.edit_user, name="edit_profile"),
]
