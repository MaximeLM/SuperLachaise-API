# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from superlachaise_api.models import Language, OpenStreetMapPOI, PendingModification, ArchivedModification, Setting, SyncOperation

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description',)
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'description']}),
    ]
    readonly_fields = ('created', 'modified')

class OpenStreetMapPOIAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'historic', 'wikipedia', 'wikidata', 'wikimedia_commons', 'latitude', 'longitude', 'created', 'modified')
    ordering = ('name', 'id',)
    search_fields = ('name', 'id', 'wikidata', 'wikimedia_commons',)
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'id', 'latitude', 'longitude']}),
        (u'Tags', {'fields': ['historic', 'wikipedia', 'wikidata', 'wikimedia_commons']}),
    ]
    readonly_fields = ('created', 'modified')

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

class SyncOperationAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_executed', 'last_result', 'description', 'created', 'modified')
    ordering = ('name', )
    search_fields = ('name', )
    readonly_fields = ('last_executed', 'last_result', 'created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'last_executed', 'last_result', 'description']}),
    ]
    
    def perform_sync(self, request, queryset):
        for sync_operation in queryset:
            try:
                sync_operation.perform_sync()
            except Exception as exception:
                print exception
    
    actions=[perform_sync]

admin.site.register(Language, LanguageAdmin)
admin.site.register(OpenStreetMapPOI, OpenStreetMapPOIAdmin)
admin.site.register(PendingModification, PendingModificationAdmin)
admin.site.register(ArchivedModification, ArchivedModificationAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(SyncOperation, SyncOperationAdmin)
