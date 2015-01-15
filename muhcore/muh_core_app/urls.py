from django.conf.urls import patterns, url

from muh_core_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<guilda_id>\d+)/$', views.guilda, name='guilda'),
    url(r'^personagem/(?P<personagem_id>\d+)/$', views.personagem, name='personagem')
)
