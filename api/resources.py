from tastypie.resources import ModelResource
from weightlog.models import Workout

class WorkoutResource(ModelResource):
    class Meta:
        queryset = Workout.objects.all()
        allowed_methods = ['get']

