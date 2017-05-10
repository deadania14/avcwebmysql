from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^update_profile/(?P<pk>[\-\w]+)/$', views.edit_user, name="edit_profile"),
]
