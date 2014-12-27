from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^login/', 'ask.views.login'), 
    url(r'^signup/', 'ask.views.signup'),
    url(r'^', include('ask.urls')),
    #url(r'^methods/', include('methods.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', 'ask.views.index'),
)
