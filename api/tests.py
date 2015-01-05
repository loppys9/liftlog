from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from tastypie.test import ResourceTestCase
from weightlog.models import Workout, Excercise, LiftEntry
from django.db.utils import DataError

#server_url = '127.0.0.1:8000/api/v1/'
server_url = '/api/v1/'
setup_done = 0

dbg = 0

def dbg_print(p):
    if dbg == 1:
        print(p)

class WorkoutResourceTest(ResourceTestCase):
    #fixtures = ['test_entries.json']
    resource_url = server_url + 'workout/'


    def setUp(self):
        global setup_done
        super(WorkoutResourceTest,self).setUp()
        
        if setup_done == 0:
            #print("Setup!!!", setup_done)
            setup_done = 0

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
            self.user2 = User.objects.create_user(self.uname1, 'testy@logyourlift.com', self.pass1)

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
        #print("\n\n-----get list unauthed")
        resp = self.api_client.get(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_list_json(self):
        #print("\n\n-----get list json")
        resp = self.api_client.get(self.resource_url, format='json', authentication=self.get_credentials())
        #print(self.deserialize(resp))
        #print('length ' + str(len(self.deserialize(resp)['objects'])))
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthorized(self):
        #print("\n\n-----post list unauth")
        resp = self.api_client.post(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_post_authorized(self):
        #print("\n\n-----post list auth")
        num = Workout.objects.count()
        resp = self.api_client.post(self.resource_url, format='json', data=self.post_data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(Workout.objects.count(), num+1)

    def test_name_too_long(self):
        #print("\n\n-----name too long")
        p1 = { 'name': 'o'*251,
                'date': str(datetime.now())[:10],
                'descr': 'Overtime'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    def test_wrong_date_format(self):
        #print("\n\n-----wrong data format")
        p1 = { 'name': 'rdio',
                'date': str(datetime.now()),
                'descr': 'rdio stream'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    def test_user_info(self):
        #print("\n\n-----user info")
        auth =  self.create_basic(username=self.uname1, password=self.pass1)
        #auth =  self.create_basic(username=self.username, password=self.password)
        resp = self.api_client.get(self.resource_url, format='json', authentication=auth)
        #print(self.deserialize(resp))
        self.assertEqual(len(self.deserialize(resp)['objects']), 0 )
        
    #def test_cross_site_scripting(self):
        #print("\n\n-----xss")
        #TODO implement this
     #   pass

class ExcerciseResourceTest(ResourceTestCase):
    #fixtures = ['test_entries.json']
    resource_url = server_url + 'excercise/'


    def setUp(self):
        global setup_done
        super(ExcerciseResourceTest,self).setUp()
        
        group, created = Group.objects.get_or_create(name="member")
        group.permissions.add(Permission.objects.get(codename='add_excercise'))
        group.permissions.add(Permission.objects.get(codename='change_excercise'))
        group.permissions.add(Permission.objects.get(codename='delete_excercise'))
        group.save()

        self.username = 'testy'
        self.password = 'testerson'
        #self.user = User.objects.create_user(self.username, 'testy@logyourlift.com', self.password)
        self.user = User.objects.create_superuser(self.username, 'testy@logyourlift.com', self.password)

        group.user_set.add(self.user)

        self.uname1 = 'tester'
        self.pass1 = 'testerson1'
        self.user2 = User.objects.create_user(self.uname1, 'testy@logyourlift.com', self.pass1)

        self.post_data = {
                'name': 'bench',
                'etype': 'chest',
                'descr': "benching"
                }

        e = Excercise(name="blah", etype='meh', descr='The best')
        e.save()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthorized(self):
        #print("\n\nExc-----get list unauthed")
        resp = self.api_client.get(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_list_json(self):
        #print("\n\nExc-----get list json")
        resp = self.api_client.get(self.resource_url, format='json', authentication=self.get_credentials())
        #print(self.deserialize(resp))
        #print('length ' + str(len(self.deserialize(resp)['objects'])))
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthorized(self):
        #print("\n\nExc-----post list unauth")
        resp = self.api_client.post(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_post_authorized(self):
        #print("\n\nExc-----post list auth")
        num = Excercise.objects.count()
        resp = self.api_client.post(self.resource_url, format='json', data=self.post_data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(Excercise.objects.count(), num+1)

    def test_name_too_long(self):
        #print("\n\nExc-----name too long")
        p1 = { 'name': 'o'*251,
                'etype': 'overhead',
                'descr': 'Overtime'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    #def test_cross_site_scripting(self):
        #print("\n\n-----xss")
        #TODO implement this
     #   pass

class LiftEntryResourceTest(ResourceTestCase):
    #fixtures = ['test_entries.json']
    resource_url = server_url + 'liftentry/'


    def setUp(self):
        global setup_done
        super(LiftEntryResourceTest,self).setUp()
        
        group, created = Group.objects.get_or_create(name="member")
        group.permissions.add(Permission.objects.get(codename='add_liftentry'))
        group.permissions.add(Permission.objects.get(codename='change_liftentry'))
        group.permissions.add(Permission.objects.get(codename='delete_liftentry'))
        group.save()

        self.username = 'testy'
        self.password = 'testerson'
        self.user = User.objects.create_user(self.username, 'testy@logyourlift.com', self.password)

        group.user_set.add(self.user)

        self.uname1 = 'tester'
        self.pass1 = 'testerson1'
        self.user2 = User.objects.create_user(self.uname1, 'testy@logyourlift.com', self.pass1)

        w = Workout(name="blah", date=datetime.now(), descr='The best', user=self.user)
        w.save()
        e = Excercise(name="blah", etype='meh', descr='The best')
        e.save()
        le = LiftEntry(weight="22.5", units="lbs", sets="4", reps="9", user=self.user,
                excercise=e, workout=w)
        le.save()

        self.post_data = {
                'weight': '32.7',
                'units': 'kg',
                'sets': '4',
                'reps': '9',
                'workout':server_url + 'workout/' + str(w.id) + '/',
                'excercise':server_url + 'excercise/' + str(e.id) + '/',
                }

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthorized(self):
        dbg_print("\n\nLE-----get list unauthed")
        resp = self.api_client.get(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_list_json(self):
        dbg_print("\n\nLE-----get list json")
        resp = self.api_client.get(self.resource_url, format='json', authentication=self.get_credentials())
        #print(self.deserialize(resp))
        #print('length ' + str(len(self.deserialize(resp)['objects'])))
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthorized(self):
        dbg_print("\n\nLE-----post list unauth")
        resp = self.api_client.post(self.resource_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_post_authorized(self):
        dbg_print("\n\nLE-----post list auth")
        num = LiftEntry.objects.count()
        resp = self.api_client.post(self.resource_url, format='json', data=self.post_data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(LiftEntry.objects.count(), num+1)

    def test_invalid_weight(self):
        dbg_print("\n\nLE-----invalid weight")
        w = Workout(name="olah", date=datetime.now(), descr='The best', user=self.user)
        w.save()
        e = Excercise(name="bench", etype='best', descr='The best')
        e.save()
        p1 = { 'weight': '-100.7',
               'units': 'kg',
               'sets': '2',
               'reps': '8',
               'workout':server_url + 'workout/' + str(w.id) + '/',
               'excercise':server_url + 'excercise/' + str(e.id) + '/',
              }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    def test_wrong_date_format(self):
        dbg_print("\n\nLE-----wrong data format")
        p1 = { 'name': 'rdio',
                'date': str(datetime.now()),
                'descr': 'rdio stream'
                }
        resp = self.api_client.post(self.resource_url, format='json', data=p1, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)

    def test_user_info(self):
        dbg_print("\n\nLE-----user info")
        auth =  self.create_basic(username=self.uname1, password=self.pass1)
        #auth =  self.create_basic(username=self.username, password=self.password)
        resp = self.api_client.get(self.resource_url, format='json', authentication=auth)
        #print(self.deserialize(resp))
        self.assertEqual(len(self.deserialize(resp)['objects']), 0 )
        
    #def test_cross_site_scripting(self):
        #print("\n\n-----xss")
        #TODO implement this
     #   pass

