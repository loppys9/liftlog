from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api.resources import WorkoutResource, ExcerciseResource, ExcerciseSearchResource, LiftEntryResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(LiftEntryResource())
v1_api.register(WorkoutResource())
v1_api.register(ExcerciseResource())
v1_api.register(ExcerciseSearchResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liftlog.views.home', name='home'),
    # url(r'^liftlog/', include('liftlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^', include('weightlog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
