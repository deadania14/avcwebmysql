from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list_article/$', views.list_article, name='list_article'),
]
