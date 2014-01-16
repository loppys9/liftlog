from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField('workout date')
	added = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=250)
	descr = models.TextField('description',blank=True)

	def __unicode__(self):
		return self.name

class Excercise(models.Model):
	name = models.CharField(max_length=250)
	etype = models.CharField('Type', max_length=250,blank=True)
	descr = models.TextField('description',blank=True)

	def __unicode__(self):
		return self.name

class LiftEntry(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()
	workouts = models.ForeignKey(Workout)
	excercise = models.ForeignKey(Excercise)
	weight = models.FloatField()
	units  = models.CharField(max_length=10)
	sets = models.IntegerField()
	reps = models.IntegerField()
	note = models.TextField(blank=True)

	def __unicode__(self):
		return self.excercise.name

