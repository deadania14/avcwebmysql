from django.conf.urls import url
from . import views
from . import views as core_views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    #about
    url(r'^about/$', views.about, name="about"),
    #konser
    url(r'^konser/$', views.konser, name="konser"),
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
    url(r'^update_profile/(?P<pk>[0-9]+)/$', views.edit_user, name="edit_profile"),

    #tutor
    url(r'^tutor/$', views.home_tutor, name='home_tutor'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
]
