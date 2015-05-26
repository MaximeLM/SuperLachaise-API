# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import translation

from superlachaise_api.models import Language, OpenStreetMapPOI, PendingModification, ArchivedModification, Setting, AdminCommand

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description',)
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'description']}),
    ]
    readonly_fields = ('created', 'modified')

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
        url = 'https://www.openstreetmap.org/{type}/{id}'.format(type=obj.type, id=str(obj.id))
        return mark_safe("<a href='%s'>%s</a>" % (url, str(obj.id)))
    openstreetmap_link.allow_tags = True
    openstreetmap_link.short_description = 'OpenStreetMap'
    
    def wikipedia_link(self, obj):
        if obj.wikipedia:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=language, name=unicode(obj.wikipedia))
            return mark_safe("<a href='%s'>%s</a>" % (url, unicode(obj.wikipedia)))
        else:
            return None
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = 'wikipedia'
    
    def wikidata_link(self, obj):
        if obj.wikidata:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.wikidata), language=language)
            return mark_safe("<a href='%s'>%s</a>" % (url, unicode(obj.wikidata)))
        else:
            return None
    wikidata_link.allow_tags = True
    wikidata_link.short_description = 'wikidata'
    
    def wikimedia_commons_link(self, obj):
        if obj.wikimedia_commons:
            url = u'http://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons))
            return mark_safe("<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons)))
        else:
            return None
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = 'wikimedia commons'

class PendingModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'new_values', 'created', 'modified')
    ordering = ('target_object_class', 'target_object_id', )
    search_fields = ('target_object_class', 'target_object_id', 'action', 'new_values', )
    readonly_fields = ('target_object_link', 'created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (u'Target object', {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (u'Modification', {'fields': ['action', 'new_values']}),
    ]
    
    def target_object_link(self, obj):
        if obj.target_object():
            app_name = obj._meta.app_label
            reverse_name = obj.target_object_class.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args = (obj.target_object().id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, unicode(obj.target_object())))
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

class ArchivedModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'new_values', 'created', 'modified')
    ordering = ('-created', )
    search_fields = ('target_object_class', 'target_object_id', 'action', 'new_values', )
    readonly_fields = ('target_object_link', 'created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (u'Target object', {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (u'Modification', {'fields': ['action', 'new_values']}),
    ]
    
    def target_object_link(self, obj):
        if obj.target_object():
            app_name = obj._meta.app_label
            reverse_name = obj.target_object_class.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args = (obj.target_object().id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, unicode(obj.target_object())))
        else:
            return None
    target_object_link.allow_tags = True

class SettingAdmin(admin.ModelAdmin):
    list_display = ('category', 'key', 'value', 'description', 'created', 'modified')
    ordering = ('category', 'key', )
    search_fields = ('category', 'key', 'value', 'description', )
    readonly_fields = ('created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['category', 'key', 'value', 'description']}),
    ]

class AdminCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_executed', 'last_result', 'description', 'created', 'modified')
    ordering = ('name', )
    search_fields = ('name', )
    readonly_fields = ('last_executed', 'last_result', 'created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'last_executed', 'last_result', 'description']}),
    ]
    
    def perform_command(self, request, queryset):
        for admin_command in queryset:
            try:
                admin_command.perform_command()
            except Exception as exception:
                print exception
    
    actions=[perform_command]

admin.site.register(Language, LanguageAdmin)
admin.site.register(OpenStreetMapPOI, OpenStreetMapPOIAdmin)
admin.site.register(PendingModification, PendingModificationAdmin)
admin.site.register(ArchivedModification, ArchivedModificationAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(AdminCommand, AdminCommandAdmin)
