from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.list_article, name='list_article'),
    #/new_article
    url(r'^article/new/$', views.new_article, name='new_article'),
    #/article_detail
    url(r'^article/detail-(?P<article_id>[0-9]+)/$', views.detail_article, name='detail_article'),
    #/article_edit
    url(r'^article/detail-(?P<article_id>[0-9]+)/edit/$', views.edit_article, name='edit_article'),
    #practice_schedules
    url(r'^latihan/$', views.list_practice, name='list_practice'),
    #practice_absensi
    url(r'^latihan/absensi/(?P<practice_id>[0-9]+)/$', views.absensi_practice, name='absensi_practice'),
]
