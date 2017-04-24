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
    #hpd
    url(r'^hpd/$', views.home_hpd, name='home_hpd'),
    #Keuangan
    url(r'^keuangan/$', views.home_keuangan, name='home_keuangan'),
    #confirmation_payments
    url(r'^keuangan/konfirmasi_pembayaran/(?P<payment_id>[0-9]+)/$', views.confirmation_payment, name='confirmation_payment'),
    #Cancel_payments
    url(r'^keuangan/gagalkan_pembayaran/(?P<payment_id>[0-9]+)/$', views.cancel_payment, name='cancel_payment'),
    #Inventaris
    url(r'^inventaris/$', views.home_inventaris, name='home_inventaris'),
    #psdm
    url(r'^psdm/$', views.home_psdm, name='home_psdm'),
    #tutor
    url(r'^tutor/$', views.home_tutor, name='home_tutor'),
    #/new_kelas
    url(r'^psdm/new_kelas/$', views.new_kelas, name='new_kelas'),
    #/edit_kelas
    url(r'^psdm/kelas/-(?P<kelas_id>[0-9]+)/edit/$', views.edit_kelas, name='edit_kelas'),
    #/new_schedule
    url(r'^psdm/new_schedule/$', views.new_schedule, name='new_schedule'),
    #/edit_attendance
    url(r'^psdm/edit_attendance/(?P<attendance_id>[0-9]+)/$', views.edit_attendance, name='edit_attendance'),
    #/new_attendance
    url(r'^psdm/new_attendance/$', views.new_attendance, name='new_attendance'),
    #/detail_article
    url(r'^psdm/detail_schedule/(?P<schedule_id>[0-9]+)/$', views.detail_schedule, name='detail_schedule'),
    #/schedule_edit
    url(r'^psdm/edit_schedule/(?P<schedule_id>[0-9]+)/$', views.edit_schedule, name='edit_schedule'),
    #/schedule_delete
    url(r'^psdm/delete_schedule/(?P<schedule_id>[0-9]+)/$', views.delete_schedule, name='delete_schedule'),
    #acara
    url(r'^acara/$', views.home_acara, name='home_acara'),
    #confirmation_event
    url(r'^acara/konfirmasi_event/(?P<event_id>[0-9]+)/$', views.confirmation_event, name='confirmation_event'),
    #cancel event
    url(r'^acara/tolak_tawaran/(?P<event_id>[0-9]+)/$', views.cancel_event, name='cancel_event'),
]
