from django.shortcuts import render, get_object_or_404
from weightlog.models import Workout, Excercise
from django.http import HttpResponse


def workout(request):
	"""Workout page"""
	context = {}
	return render(request, 'weightlog/newworkout.html', context)

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
