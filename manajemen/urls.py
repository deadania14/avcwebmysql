from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #edit_user
    url(r'^edit_user/(?P<user_id>[0-9]+)/$', views.edit_user, name='edit_user'),

    #HPD V
    url(r'^hpd/$', views.home_hpd, name='home_hpd'),
    #/new_article V
    url(r'^hpd/article/new/$', views.new_article, name='new_article'),
    #/article_detail V
    url(r'^hpd/article/detail-(?P<article_id>[0-9]+)/$', views.detail_article, name='detail_article'),
    #/article_edit V
    url(r'^hpd/article/detail-(?P<article_id>[0-9]+)/edit/$', views.edit_article, name='edit_article'),
    url(r'^hpd/main-article/detail-(?P<article_id>[0-9]+)/edit/$', views.edit_mainarticle, name='edit_mainarticle'),
    #/edit_contact
    url(r'^hpd/contact/edit/$', views.edit_contact, name='edit_contact'),


    #psdm V
    url(r'^psdm/$', views.home_psdm, name='home_psdm'),
    #tutor
    url(r'^tutor/$', views.home_tutor, name='home_tutor'),
    #/new_kelas
    url(r'^psdm/new_kelas/$', views.new_kelas, name='new_kelas'),
    #/edit_kelas
    #url(r'^psdm/kelas/-(?P<kelas_id>[0-9]+)/edit/$', views.edit_kelas, name='edit_kelas'),
    #/new_schedule
    url(r'^psdm/new_schedule/$', views.new_schedule, name='new_schedule'),
    #/new_attendance_people
    url(r'^psdm/new_attendance_kelas/new_attendance_people/(?P<attendance_id>[0-9]+)$', views.new_attendance_people, name='new_attendance_people'),
    #/new_attendance_kelas
    url(r'^psdm/new_attendance_kelas/$', views.new_attendance_kelas, name='new_attendance_kelas'),
    #/edit_attendance
    url(r'^psdm/edit_attendance/(?P<attendance_id>[0-9]+)/$', views.edit_attendance, name='edit_attendance'),
    #/detail_schedule
    url(r'^psdm/detail_schedule/(?P<schedule_id>[0-9]+)/$', views.detail_schedule, name='detail_schedule'),
    #/schedule_edit
    url(r'^psdm/edit_schedule/(?P<schedule_id>[0-9]+)/$', views.edit_schedule, name='edit_schedule'),
    #/schedule_delete
    url(r'^psdm/delete_schedule/(?P<schedule_id>[0-9]+)/$', views.delete_schedule, name='delete_schedule'),

    #Keuangan
    url(r'^keuangan/$', views.home_keuangan, name='home_keuangan'),
    #confirmation_payments
    url(r'^keuangan/konfirmasi_pembayaran/(?P<payment_id>[0-9]+)/$', views.confirmation_payment, name='confirmation_payment'),
    #Cancel_payments
    url(r'^keuangan/gagalkan_pembayaran/(?P<payment_id>[0-9]+)/$', views.cancel_payment, name='cancel_payment'),

    #acara
    url(r'^acara/$', views.home_acara, name='home_acara'),
    #/new_event
    url(r'^acara/new_event$', views.new_event, name='new_event'),

    #confirmation_event
    url(r'^acara/konfirmasi_event/(?P<event_id>[0-9]+)/$', views.confirmation_event, name='confirmation_event'),
    #cancel event
    url(r'^acara/tolak_tawaran/(?P<event_id>[0-9]+)/$', views.cancel_event, name='cancel_event'),

    #Inventaris
    url(r'^inventaris/$', views.home_inventaris, name='home_inventaris'),
    #Inventaris_new_barang
    url(r'^inventaris/new_barang/$', views.new_barang, name='new_barang'),
    #inventaris_edit_barang
    url(r'^inventaris/edit_barang/(?P<barang_id>[0-9]+)/$', views.edit_barang, name='edit_barang'),
    #inventaris_delete_barang
    url(r'^inventaris/delete_(?P<barang_id>[0-9]+)/$', views.delete_barang, name='delete_barang'),

    #sekretaris
    url(r'^sekretaris/$', views.home_sekretaris, name='home_sekretaris'),
    #sekretaris-new meeting
    url(r'^sekretaris/new-meeting/$', views.new_meeting, name='new_meeting_note'),
    #sekretaris-edit meeting
    url(r'^sekretaris/edit_(?P<meeting_id>[0-9]+)/$', views.edit_meeting, name='edit_meeting'),
    #sekretaris-delete meeting
    url(r'^sekretaris/delete_(?P<meeting_id>[0-9]+)/$', views.delete_meeting, name='delete_meeting'),

]
