from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    #/registration
    url(r'^registration/$', views.registration, name="registration"),
    #/event_detail
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),

]
