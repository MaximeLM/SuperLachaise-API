# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models

from superlachaise_api.models import Language, OpenStreetMapPOI, OpenStreetMapPOIModification, OpenStreetMapPOILocalization, OpenStreetMapPOILocalizationModification

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description',)
    actions=None

class OpenStreetMapPOILocalizationInline(admin.StackedInline):
    model = OpenStreetMapPOILocalization
    extra = 0

class OpenStreetMapPOIModificationInline(admin.StackedInline):
    model = OpenStreetMapPOIModification
    extra = 0

class OpenStreetMapPOILocalizationModificationInline(admin.StackedInline):
    model = OpenStreetMapPOILocalizationModification
    extra = 0

class OpenStreetMapPOIAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'historic', 'wikidata', 'wikimedia_commons', 'latitude', 'longitude', 'nb_localizations', 'nb_modifications', 'created', 'modified')
    ordering = ('name', 'id',)
    search_fields = ('name', 'id', 'wikidata', 'wikimedia_commons',)
    actions=None
    fieldsets = [
        (None, {'fields': ['name', 'id', 'latitude', 'longitude']}),
        (u'Tags', {'fields': ['historic', 'wikidata', 'wikimedia_commons']}),
    ]
    inlines = [
        OpenStreetMapPOILocalizationInline,
        OpenStreetMapPOIModificationInline,
        OpenStreetMapPOILocalizationModificationInline,
    ]
    
    def nb_localizations(self, obj):
        return obj.openstreetmappoilocalization_set.count()
    nb_localizations.admin_order_field = 'openstreetmappoilocalization__count'
    
    def nb_modifications(self, obj):
        return obj.openstreetmappoimodification_set.count()
    nb_modifications.admin_order_field = 'openstreetmappoimodification__count'
    
    def get_queryset(self, request):
        qs = super(OpenStreetMapPOIAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('openstreetmappoilocalization'))
        qs = qs.annotate(models.Count('openstreetmappoimodification'))
        return qs

admin.site.register(Language, LanguageAdmin)
admin.site.register(OpenStreetMapPOI, OpenStreetMapPOIAdmin)
