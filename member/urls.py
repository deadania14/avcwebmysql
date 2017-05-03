from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^latihan/$', views.latihan, name="latihan"),
    url(r'^pembayaran/$', views.pembayaran, name="pembayaran"),
    url(r'^pengaturan/$', views.settings, name="settings"),
]
