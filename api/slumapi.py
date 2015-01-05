import slumber
import json

excercises = [
    ['Bench Press', 'Chest', 'Touch barbell to chest press'],
    ['Squat', 'Postirior Chain', 'Bend to parallel then stand up'],
    ['Deadlift', 'Postirior Chain', 'Lift barbell off the floor'],
]

url = 'http://127.0.0.1:8000/api/v1/'
auth = ('django', 'django')

api = slumber.API(url, auth=auth)

#print( api.workout.get() )

#print( api.workout.post() )

def create_excer(name, etype, descr):
    content = {'name' : name, 'etype': etype, 'descr': descr}
    return content
    #return json.dumps(content)

def pop_excer():
    #url = 'http://127.0.0.1:8000/api/v1/excercise'
    for e in excercises:
        c = create_excer(e[0], e[1], e[2])
        #print(c)
        try:
            api.excercise.post(c)
        except slumber.exceptions.HttpClientError:
            pass
        

if __name__ == '__main__':
    #print( api.excercise.get() )
    pop_excer()
