from django.conf.urls import patterns, url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from weightlog import views

router = DefaultRouter()
router.register(r'workouts', views.WorkoutViewSet)
#router.register(r'excercise', views.ExcerciseViewSet)

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		#url(r'^workout$', views.listworkout, name='listworkout'),
        #url(r'^', include(router.urls)),
		#url(r'^new_workout$', views.new_workout, name='new_workout'),
        #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'weightlog/login.html'}),
        #url(r'^workouts/$', views.WorkoutList.as_view(), name='workout-list'),
        #url(r'^workouts/(?P<pk>[0-9]+)/$', views.WorkoutDetail.as_view(), name='workout-detail'),
        #url(r'^users/$', views.UserList.as_view()),
        #url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
