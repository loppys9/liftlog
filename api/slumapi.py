#!/usr/bin/python

import slumber
import json
import csv
from itertools import islice

excer_file = 'excercises'
workout_file = 'workouts'

excercises = []

url = 'http://127.0.0.1:8000/api/v1/'
auth = ('shane', 'shane')

api = slumber.API(url, auth=auth)

#print( api.workout.get() )

#print( api.workout.post() )

previous_exc = ''

class Entry():
    excercise = ''
    weight = 0
    reps = 0
    sets = 0
    note = ''

    def __init__(self, line):
        self.add_entry_from_file(line)

    def add_entry_from_file(self, line):
        global previous_exc

        #e = line.split(',')
        e = line
        self.excercise = e[0]
        if (self.excercise == ''):
            self.excercise = previous_exc
        else:
            previous_exc = self.excercise
        self.weight = e[1]
        self.reps = e[2]
        self.sets = e[3]
        self.note = e[4]

    def e_url(self):
        eid = '-1'
        url = 'http://127.0.0.1:8000/api/v1/excercise/'
        for e in excercises:
            if e[0] == self.excercise:
                eid = e[1]
        url += str(eid) + '/'
        return url

    def to_json(self):
        return {'weight':self.weight, 'sets':self.sets, 'reps':self.reps, 'note':self.note,
                'units':'lbs', 'excercise':self.e_url()}

class Workout():
    """date = ''
    name = ''
    descr = ''"""

    def __init__(self, line):
        self.entries = []
        self.add_workout_from_file(line)

    def __iter__(self):
        self.ind = 0
        return self

    def next(self):
        if self.ind < len(self.entries):
            cur_ind = self.ind
            self.ind += 1
            json = self.entries[cur_ind].to_json()
            json['workout'] = 'http://127.0.0.1:8000/api/v1/workout/' + str(self.wid) + '/'
            #return self.entries[cur_ind]
            return json
        raise StopIteration

    def add_workout_from_file(self, line):
        #print 'entry len: ',len(self.entries)
        #w = line.split(',')
        w = line
        self.date = w[0]
        self.name = w[1]
        self.descr = w[2]

    def add_entry(self, entry):
        #print len(self.entries)
        self.entries.append(entry)

    def set_wid(self, wid):
        self.wid = wid
        pass

    def w_to_json(self):
        return {'date':self.date, 'name':self.name, 'descr':self.descr}
        

def create_excer(name, etype, descr):
    content = {'name' : name, 'etype': etype, 'descr': descr}
    return content
    #return json.dumps(content)

def get_workouts():
    new = False
    entries = False
    ws = []

    with open(workout_file, 'r') as f:
        #for w in f.read().splitlines():
        reader = csv.reader(f)
        for w in reader:
            if w[0] == 'workout:':
                new = True
                entries = False
                continue
            if w[0] == 'entries:':
                new = False
                entries = True
                continue

            if new and (not entries):
                ws.append(Workout(w))
            if entries and (not new):
                ws[-1].add_entry(Entry(w))

    return ws

def get_excercises():
    #f = open(excer_file, 'r')
    first = True
    excer = []
    
    with open(excer_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if first:
                first = False
                continue
            excer.append(row)

    return excer

def pop_excer():
    #url = 'http://127.0.0.1:8000/api/v1/excercise'
    excer = get_excercises()
    
    for e in excer:
        c = create_excer(e[0], e[1], e[2])
        try:
            print 'Aadding: ', e[0]
            api.excercise.post(c)
        except slumber.exceptions.HttpClientError:
            pass

def pop_workouts():
    ws = get_workouts()

    for w in ws:
        d = w.w_to_json()
        try:
            print 'Adding: ', w.name
            rsp = api.workout.post(d)
            w.set_wid(rsp['id'])
            for x in w:
                rsp = api.liftentry.post(x)
        except slumber.exceptions.HttpClientError as e:
            pass
        

if __name__ == '__main__':
    es = api.excercise.get()
    for e in es['objects']:
        excercises.append([e['name'], e['id']])

    pop_excer()
    pop_workouts()

