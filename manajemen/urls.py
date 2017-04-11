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
    #practice_absensi
    url(r'^latihan/absensi/(?P<practice_id>[0-9]+)/$', views.absensi_practice, name='absensi_practice'),
    #psdm
    url(r'^psdm/$', views.home_psdm, name='home_psdm'),
    #Keuangan
    url(r'^keuangan/$', views.home_keuangan, name='home_keuangan'),
    #/new_article
    url(r'^schedule/new/$', views.new_schedule, name='new_schedule'),
    #/schedule_edit
    url(r'^schedule/(?P<schedule_id>[0-9]+)/edit/$', views.edit_schedule, name='edit_schedule'),
]
