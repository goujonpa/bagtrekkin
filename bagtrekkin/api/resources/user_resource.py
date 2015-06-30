from django.contrib.auth.models import User

from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
