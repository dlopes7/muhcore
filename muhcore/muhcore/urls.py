from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^guildas/', include('muh_core_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)