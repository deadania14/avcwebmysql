from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.list_article, name='list_article'),
    #/article_detail
    url(r'^article/detail-(?P<article_id>[0-9]+)/$', views.detail_article, name='detail_article'),
    #/new_article
    url(r'^article/new/$', views.new_article, name='new_article'),
    #/url(r'^article/edit-(?P<pk>\d+)/$', views.edit_article, name='edit_article'),
]
