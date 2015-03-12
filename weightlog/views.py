from django.shortcuts import render, get_object_or_404
from weightlog.models import Workout, Excercise
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

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

@login_required
def index(request):
	w = Workout.objects.all()
	l = []
	e = []
	num = 3
	for x in w:
		e = list(x.liftentry_set.all()[:num])
		for i in range(3-len(e)):
				e.append(None)
		l.append( [x, e] )
	context = { 'w': l }
	return render(request, 'weightlog/tmp.html', context)
