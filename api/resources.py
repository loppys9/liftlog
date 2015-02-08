from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, SessionAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from tastypie import fields
from weightlog.models import Workout, Excercise, LiftEntry
from django.contrib.auth.models import User
from time import strptime
from api.auth import WorkoutAuthorization, ExcerciseAuthorization, LiftEntryAuthorization
import json

class WorkoutValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        if len(bundle.data['name']) > 250:
            errors['name'] = ['Name length too long.']
        try:
            #print(bundle.data['date'])
            strptime(bundle.data['date'], '%Y-%m-%d')
        except:
            errors['date'] = ['Date format incorrect. Please use %Y-%M-%D, Year-Month-Day']
        return errors

class WorkoutResource(ModelResource):
    class Meta:
        queryset = Workout.objects.all()
        allowed_methods = ['get','post']
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        #authorization = DjangoAuthorization()
        authorization = WorkoutAuthorization()
        validation = WorkoutValidation()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(WorkoutResource, self).obj_create(bundle, user=bundle.request.user)

class ExcerciseValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        if len(bundle.data['name']) > 250:
            errors['name'] = ['Name length too long.']
        if len(bundle.data['etype']) > 250:
            errors['etype'] = ['Excercise type too long.']
        if Excercise.objects.filter(name=bundle.data['name']).exists():
            errors['name'] = ['Excercise already exists']
        return errors

class ExcerciseResource(ModelResource):
    class Meta:
        queryset =Excercise.objects.all()
        allowed_methods = ['get', 'post']
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        #authorization = DjangoAuthorization()
        authorization = ExcerciseAuthorization()
        validation = ExcerciseValidation()
        #always_return_data = True

class ExcerciseSearchValidation(Validation):
    def is_valid(self, bundle, request=None):
        print('is valid')
        errors = {}
        print( request)
        if len(bundle.data['name']) > 250:
            errors['name'] = ['Name length too long.']
        return errors

class ExcerciseSearchResource(ModelResource):
    class Meta:
        #queryset =Excercise.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        authorization = DjangoAuthorization()
        #authorization = ExcerciseAuthorization()
        #validation = ExcerciseSearchValidation()
        always_return_data = True
        
    def get_list(self, request, **kwargs):
        phrase = request.GET.get('term')
        if phrase and (len(phrase) < 250):
            #change startswith if a different search is desired.
            excercise = list(Excercise.objects.filter(name__startswith=phrase).values('id', 'name'))
            print(excercise)
            #return self.create_response(request, {'excercise': excercise})
            return self.create_response(request, json.dumps(excercise))

    def post_list(self, request, **kwargs):
        phrase = request.POST.get('q')
        if phrase and (len(phrase) < 250):
            #change startswith if a different search is desired.
            excercise = list(Excercise.objects.filter(name__startswith=phrase).values('id', 'name'))
            return self.create_response(request, {'excercise': excercise})

class LiftEntryValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        d = bundle.data
        try:
            weight = float(d['weight'])
            sets = int(d['sets'])
            reps = int(d['reps'])
        except ValueError:
            errors['input'] = ['Wrong input type']
            return errors
        #print(bundle.data)
        if weight < 0.0:
            errors['weight'] = ['Not a valid weight']
        if weight > 10000.0:
            errors['weight'] = ['Come on, be serious!']
        if sets < 0 or sets > 1000:
            errors['sets'] = ['Sets are between 0 and 1000']
        if reps < 0 or reps > 1000:
            errors['reps'] = ['Reps are between 0 and 1000']
        return errors

class LiftEntryResource(ModelResource):
    workout = fields.ForeignKey(WorkoutResource, 'workout')
    excercise = fields.ForeignKey(ExcerciseResource, 'excercise')

    class Meta:
        queryset = LiftEntry.objects.all()
        allowed_methods = ['get','post']
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        authorization = LiftEntryAuthorization()
        validation = LiftEntryValidation()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(LiftEntryResource, self).obj_create(bundle, user=bundle.request.user)

