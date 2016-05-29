from django.shortcuts import render, get_object_or_404
from weightlog.models import Workout, Excercise, LiftEntry
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from weightlog.serializers import WorkoutSerializer, LiftEntrySerializer
from weightlog.serializers import UserSerializer
from weightlog.serializers import ExcerciseSerializer, ExcerciseSearchSerializer
from weightlog.permissions import IsOwner

logger = logging.getLogger(__name__)

#class ExcerciseSearchViewSet(viewsets.ReadOnlyModelViewSet):
class ExcerciseSearchViewSet(viewsets.ModelViewSet):
    queryset = Excercise.objects.all()
    serializer_class = ExcerciseSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        q = request.query_params['q']
        #print(q)
        #print(request.query_params)
        excercises = Excercise.objects.filter(name__istartswith=q)
        es = ExcerciseSearchSerializer(excercises, many=True)
        print(excercises)
        return Response(es.data)

class ExcerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Excercise.objects.all()
    serializer_class = ExcerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        user = self.request.user
        return Workout.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LiftEntryViewSet(viewsets.ModelViewSet):
    queryset = LiftEntry.objects.all()
    serializer_class = LiftEntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        user = self.request.user
        return LiftEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@login_required
def listworkout(request):
    """Workout page"""
    context = {}
    return render(request, 'weightlog/listworkout.jade', context)
    #return render(request, 'weightlog/newworkout.html', context)

@login_required
def new_workout(request):
    """New workout page"""
    context = {}
    return render(request, 'weightlog/newworkout.jade', context)
    #return render(request, 'weightlog/newworkout.html', context)

#@login_required
def index(request):
    print("Maybe...")
    context = {}
    return render(request, 'index.html', context)

