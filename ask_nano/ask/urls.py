from django.conf.urls import patterns, url

from ask import views

urlpatterns = patterns('',
	url(r'^question/(?P<quest>\d+)/$', 'ask.views.question', name='question'),
	url(r'^add/', 'ask.views.add', name='add'),
	url(r'^response/(?P<quest>\d+)/$', 'ask.views.response', name='response'),
	url(r'^$', views.index, name='index'),
)