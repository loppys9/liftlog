from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, SessionAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from weightlog.models import Workout
from django.contrib.auth.models import User
from time import strptime

class WorkoutValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        if len(bundle.data['name']) > 250:
            errors['name'] = ['Name length too long.']
        try:
            print(bundle.data['date'])
            strptime(bundle.data['date'], '%Y-%m-%d')
        except:
            print("there was a problem with the date")
            errors['date'] = ['Date format incorrect. Please use %Y-%M-%D, Year-Month-Day']
        return errors

class WorkoutResource(ModelResource):
    class Meta:
        queryset = Workout.objects.all()
        allowed_methods = ['get','post']
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        authorization = DjangoAuthorization()
        validation = WorkoutValidation()

    def obj_create(self, bundle, **kwargs):
        print("creating...")
        return super(WorkoutResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        print("auth lims...")
        print(request)
        return object_list.filter(user=request.user)

