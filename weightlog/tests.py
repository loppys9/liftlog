"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User
from weightlog.models import Workout
from datetime import datetime

class WorkoutModelTest(TestCase):
    def setUp(self):
        self.username = 'testy'
        self.password = 'testerson'
        self.user = User.objects.create_user(self.username, 'testy@logyourlift.com', self.password)

    def test_workout_without_user(self):
        n = None
        try:
            n = Workout(name="blah", date=datetime.now())
            n.save()
        except IntegrityError:
            self.assertEqual(None, None)
        else:
            self.assertEqual(False, True)

    def test_workout_with_user(self):
        n = None
        n = Workout(user_id=self.user.id, name="one two three", date=str(datetime.now())[:10])
        n.save()
        self.assertNotEqual(n,None)

