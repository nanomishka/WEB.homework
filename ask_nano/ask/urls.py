from django.conf.urls import patterns, url

from ask import views

urlpatterns = patterns('',
	url(r'^question/(?P<quest>\d+)/$', 'ask.views.question', name='question'),
	url(r'^add/', 'ask.views.add', name='add'),
	url(r'^response/(?P<quest>\d+)/$', 	'ask.views.response', name='response'),
	url(r'^profile/$', 'ask.views.profile', name='profile'),
	url(r'^like/$', 'ask.views.like', name='like'),
	url(r'^$', views.index, name='index'),
)