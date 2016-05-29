from django.contrib import admin
from weightlog.models import Workout
from weightlog.models import Excercise
from weightlog.models import LiftEntry

class ExcerciseAdmin(admin.ModelAdmin):
	list_display = ('name',)	

class LiftEntryInline(admin.StackedInline):
	model = LiftEntry
	extra = 1

class WorkoutAdmin(admin.ModelAdmin):
	list_display = ('name',)
	inlines = [LiftEntryInline]
	
class LiftEntryAdmin(admin.ModelAdmin):
	list_display = ('excercise',)

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Excercise, ExcerciseAdmin)
admin.site.register(LiftEntry, LiftEntryAdmin)
