# -*- encoding: utf-8 -*-
from django.contrib import admin
from bagtrekkin.models import Compagnies, Luggages


class CompagniesAdmin(admin.ModelAdmin):
    list_display = ("id_company", "name")
    exclude = ("id_company",)


class LuggagesAdmin(admin.ModelAdmin):
    list_display = ("id_passenger", "material_number")

admin.site.register(Compagnies, CompagniesAdmin)
admin.site.register(Luggages, LuggagesAdmin)
