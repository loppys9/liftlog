from django.forms import widgets
from rest_framework import serializers
from weightlog.models import Workout, Excercise, LiftEntry
from django.contrib.auth.models import User

class ExcerciseSearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Excercise
        fields = ('name','id')

class ExcerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Excercise
        fields = ('name','etype', 'descr')

class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workout
        fields = ('id','date', 'name', 'descr')

class LiftEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LiftEntry
        fields = ('workout', 'excercise', 'units', 'weight', 'sets', 'reps', 'note')
        
class UserSerializer(serializers.ModelSerializer):
    #workouts = serializers.PrimaryKeyRelatedField(many=True, queryset=Workout.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username')
