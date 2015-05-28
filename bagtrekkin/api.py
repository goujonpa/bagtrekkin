# -*- encoding: utf-8 -*-
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models import Materials


class MaterialsResource(ModelResource):

    class Meta:
        queryset = Materials.objects.all()
        resource_name = 'materials'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
