from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from tastypie.test import ResourceTestCase
from weightlog.models import Workout
from django.db.utils import DataError

#server_url = '127.0.0.1:8000/api/v1/'
server_url = '/api/v1/'

class WorkoutResourceTest(ResourceTestCase):
    #fixtures = ['test_entries.json']
    resource_url = server_url + 'workout/'


    def setUp(self):
        super(WorkoutResourceTest,self).setUp()

        group, created = Group.objects.get_or_create(name="member")
        group.permissions.add(Permission.objects.get(codename='add_workout'))
        group.permissions.add(Permission.objects.get(codename='change_workout'))
        group.permissions.add(Permission.objects.get(codename='delete_workout'))
        group.save()

        self.username = 'testy'
        self.password = 'testerson'
        self.user = User.objects.create_user(self.username, 'testy@logyourlift.com', self.password)

        group.user_set.add(self.user)

        self.uname1 = 'tester'
        self.pass1 = 'testerson1'
        self.user = User.objects.create_user(self.uname1, 'testy@logyourlift.com', self.pass1)

        self.post_data = {
                'name': 'goodness',
                'date': str(datetime.now())[:10],
                'descr': "Something new"
                }

        w = Workout(name="blah", date=datetime.now(), descr='The best', user=self.user)
        w.save()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthorized(self):
        resp = self.api_client.get(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_list_json(self):
        resp = self.api_client.get(self.resource_url, format='json', authentication=self.get_credentials())
        #print(self.deserialize(resp))
        #print('length ' + str(len(self.deserialize(resp)['objects'])))
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthorized(self):
        resp = self.api_client.post(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_post_authorized(self):
        num = Workout.objects.count()
        resp = self.api_client.post(self.resource_url, format='json', data=self.post_data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(Workout.objects.count(), num+1)

    def test_name_too_long(self):
        p1 = { 'name': 'o'*251,
                'date': str(datetime.now())[:10],
                'descr': 'Overtime'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    def test_name_too_long(self):
        p1 = { 'name': 'rdio',
                'date': str(datetime.now()),
                'descr': 'rdio stream'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

