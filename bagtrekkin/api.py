from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models import Material


class MaterialsResource(ModelResource):

    class Meta:
        queryset = Material.objects.all()
        resource_name = 'materials'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
