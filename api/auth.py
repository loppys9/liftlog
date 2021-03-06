from tastypie.authorization import DjangoAuthorization
#from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

def dbg_print(x):
    #print x
    pass

class LiftEntryAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        dbg_print('read_list')
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        dbg_print('LE read_detail')
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        dbg_print('create_list')
        return Unauthorized("Can't create list yet")

    def create_detail(self, object_list, bundle):
        dbg_print('create_detail')
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        dbg_print('update_list')
        return Unauthorized("Can't update list yet")

    def update_detail(self, object_list, bundle):
        dbg_print('update_detail')
        return Unauthorized("Can't update detail yet")

    def delete_list(self, object_list, bundle):
        dbg_print('delete_list')
        return Unauthorized("Can't delete list yet")

    def delete_detail(self, object_list, bundle):
        dbg_print('delete_detail')
        return Unauthorized("Can't delete detail yet")

class WorkoutAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        dbg_print('read_list')
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        dbg_print('WA read_detail')
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        dbg_print('create_list')
        return Unauthorized("Can't create list yet")

    def create_detail(self, object_list, bundle):
        dbg_print('create_detail')
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        dbg_print('update_list')
        return Unauthorized("Can't update list yet")

    def update_detail(self, object_list, bundle):
        dbg_print('update_detail')
        return Unauthorized("Can't update detail yet")

    def delete_list(self, object_list, bundle):
        dbg_print('delete_list')
        return Unauthorized("Can't delete list yet")

    def delete_detail(self, object_list, bundle):
        dbg_print('delete_detail')
        return Unauthorized("Can't delete detail yet")

class ExcerciseAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        dbg_print('EA read_list')
        return object_list

    def read_detail(self, object_list, bundle):
        dbg_print('EA read_detail')
        return bundle.request.user != None

    def create_list(self, object_list, bundle):
        dbg_print('create_list')
        return Unauthorized("Can't create list yet")

    def create_detail(self, object_list, bundle):
        dbg_print('create_detail')
        #dbg_print(bundle.request.user.is_staff)
        return bundle.request.user.is_staff
        #return Unauthorized("Can't create list yet")
        #return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        dbg_print('update_list')
        return Unauthorized("Can't update list yet")

    def update_detail(self, object_list, bundle):
        dbg_print('update_detail')
        return Unauthorized("Can't update detail yet")

    def delete_list(self, object_list, bundle):
        dbg_print('delete_list')
        return Unauthorized("Can't delete list yet")

    def delete_detail(self, object_list, bundle):
        dbg_print('delete_detail')
        return Unauthorized("Can't delete detail yet")

