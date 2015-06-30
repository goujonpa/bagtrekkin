from tastypie.authorization import Authorization


class EmployeeAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        if bundle.request.path == '/api/v1/employee/schema/':
            return True
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
