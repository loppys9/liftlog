#!/usr/bin/python

import slumber
import json
from itertools import islice

excer_file = 'excercises'
workout_file = 'workouts'

url = 'http://127.0.0.1:8000/api/v1/'
auth = ('django', 'django')

api = slumber.API(url, auth=auth)

#print( api.workout.get() )

#print( api.workout.post() )

def create_excer(name, etype, descr):
    content = {'name' : name, 'etype': etype, 'descr': descr}
    return content
    #return json.dumps(content)

def get_workouts():
    new = False
    entries = False

    with open(workout_file, 'r') as f:
        for w in f.read().splitlines():
            #print new, entries
            if new and (not entries):
                print w

            if w == 'workout:':
                new = True
                entries = False
            else:
                new = False
            if w == 'entries:':
                new = False
                entries = True

    return []

def get_excercises():
    #f = open(excer_file, 'r')
    first = True
    excer = []
    
    with open(excer_file, 'r') as f:
        for e in f.read().splitlines():
            if first:
                first = False
                continue
            excer.append(e.split(','))

    return excer

def pop_excer():
    #url = 'http://127.0.0.1:8000/api/v1/excercise'
    excer = get_excercises()
    
    for e in excer:
        #print e
        c = create_excer(e[0], e[1], e[2])
        #print(c)
        try:
            api.excercise.post(c)
        except slumber.exceptions.HttpClientError:
            pass

def pop_workouts():
    works = get_workouts()
        

if __name__ == '__main__':
    #print( api.excercise.get() )
    #pop_excer()
    pop_workouts()
