from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_nano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/', 'ask.views.login'),  
    url(r'^signup/', 'ask.views.signup'),
    url(r'^methods/', include('methods.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', 'ask.views.index'),
)
