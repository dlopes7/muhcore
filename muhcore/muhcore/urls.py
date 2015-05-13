from django.conf.urls import patterns, include, url
from django.contrib import admin

from muh_core_app import views

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^bis/', views.bis_list, name='bis_list'),
    url(r'^guildas/', include('muh_core_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)