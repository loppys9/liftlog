from django.conf.urls import patterns, url
from weightlog import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^workout$', views.listworkout, name='listworkout'),
		url(r'^new_workout$', views.new_workout, name='new_workout'),
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'weightlog/login.html'}),
)
