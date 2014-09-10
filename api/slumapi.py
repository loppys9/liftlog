import slumber


url = 'http://127.0.0.1:8000/api/v1/'
auth = ('django', 'django')

api = slumber.API(url, auth=auth)

print( api.workout.get() )

print( api.workout.post() )
