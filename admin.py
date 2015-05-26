# -*- coding: utf-8 -*-

"""
admin.py
superlachaise_api

Created by Maxime Le Moine on 26/05/2015.
Copyright (c) 2015 Maxime Le Moine.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    
    http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.safestring import mark_safe

from superlachaise_api.models import *

class AdminCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_executed', 'last_result', 'description', 'created', 'modified')
    ordering = ('name',)
    search_fields = ('name', 'description',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'last_executed', 'last_result', 'description']}),
    ]
    readonly_fields = ('last_executed', 'last_result', 'created', 'modified')
    
    def perform_command(self, request, queryset):
        for admin_command in queryset:
            try:
                admin_command.perform_command()
            except Exception as exception:
                print exception
    
    actions=[perform_command]

class OpenStreetMapPOIAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'openstreetmap_link', 'wikipedia_link', 'wikidata_link', 'wikimedia_commons_link', 'historic', 'latitude', 'longitude', 'created', 'modified')
    ordering = ('name', 'id',)
    search_fields = ('name', 'type', 'id', 'wikidata', 'wikimedia_commons',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'type', 'id', 'latitude', 'longitude']}),
        (u'Tags', {'fields': ['historic', 'wikipedia', 'wikidata', 'wikimedia_commons']}),
    ]
    readonly_fields = ('created', 'modified', 'openstreetmap_link', 'wikipedia_link', 'wikidata_link', 'wikimedia_commons_link')
    
    def openstreetmap_link(self, obj):
        url = u'https://www.openstreetmap.org/{type}/{id}'.format(type=obj.type, id=unicode(obj.id))
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
    openstreetmap_link.allow_tags = True
    openstreetmap_link.short_description = 'OpenStreetMap'
    
    def wikipedia_link(self, obj):
        if obj.wikipedia:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=language, name=unicode(obj.wikipedia))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikipedia)))
        else:
            return None
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = 'wikipedia'
    
    def wikidata_link(self, obj):
        if obj.wikidata:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.wikidata), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata)))
        else:
            return None
    wikidata_link.allow_tags = True
    wikidata_link.short_description = 'wikidata'
    
    def wikimedia_commons_link(self, obj):
        if obj.wikimedia_commons:
            url = u'http://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons)))
        else:
            return None
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = 'wikimedia commons'

class PendingModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'modified_fields', 'created', 'modified')
    ordering = ('target_object_class', 'target_object_id',)
    search_fields = ('target_object_class', 'target_object_id', 'action', 'modified_fields',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (u'Target object', {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (u'Modification', {'fields': ['action', 'modified_fields']}),
    ]
    readonly_fields = ('target_object_link', 'created', 'modified')
    
    def target_object_link(self, obj):
        if obj.target_object():
            app_name = obj._meta.app_label
            reverse_name = obj.target_object_class.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.target_object().id,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.target_object())))
        else:
            return None
    target_object_link.allow_tags = True
    
    def apply_modification(self, request, queryset):
        for pending_modification in queryset:
            try:
                pending_modification.apply_modification()
            except Exception as exception:
                print exception
    
    actions=[apply_modification]

class SettingAdmin(admin.ModelAdmin):
    list_display = ('category', 'key', 'value', 'description', 'created', 'modified')
    ordering = ('category', 'key',)
    search_fields = ('category', 'key', 'value', 'description',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['category', 'key', 'value', 'description']}),
    ]
    readonly_fields = ('created', 'modified')

admin.site.register(AdminCommand, AdminCommandAdmin)
admin.site.register(OpenStreetMapPOI, OpenStreetMapPOIAdmin)
admin.site.register(PendingModification, PendingModificationAdmin)
admin.site.register(Setting, SettingAdmin)
