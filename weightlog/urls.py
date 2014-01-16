from django.conf.urls import patterns, url
from weightlog import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^workout$', views.workout, name='workout')
)
