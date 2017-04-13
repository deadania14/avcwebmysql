from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^Latihan/$', views.latihan, name="latihan"),
    url(r'^Pembayaran/$', views.pembayaran, name="pembayaran"),
    url(r'^Contacts/$', views.contact, name="contact-us"),
]
