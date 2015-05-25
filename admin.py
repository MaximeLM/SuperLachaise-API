# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from superlachaise_api.models import Language, OpenStreetMapPOI, LocalizedOpenStreetMapPOI
from superlachaise_api.models import PendingModification, ArchivedModification

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description',)
    actions=None
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'description']}),
    ]
    readonly_fields = ('created', 'modified')

class LocalizedOpenStreetMapPOIInline(admin.StackedInline):
    model = LocalizedOpenStreetMapPOI
    extra = 0
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['language', 'wikipedia']}),
    ]
    readonly_fields = ('created', 'modified')

class OpenStreetMapPOIAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'historic', 'wikidata', 'wikimedia_commons', 'latitude', 'longitude', 'localizations', 'created', 'modified')
    ordering = ('name', 'id',)
    search_fields = ('name', 'id', 'wikidata', 'wikimedia_commons',)
    actions=None
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (None, {'fields': ['name', 'id', 'latitude', 'longitude']}),
        (u'Tags', {'fields': ['historic', 'wikidata', 'wikimedia_commons']}),
    ]
    inlines = [
        LocalizedOpenStreetMapPOIInline,
    ]
    readonly_fields = ('created', 'modified')
    
    def localizations(self, obj):
        return obj.localizedopenstreetmappoi_set.count()
    localizations.admin_order_field = 'localizedopenstreetmappoi__count'
    
    def get_queryset(self, request):
        qs = super(OpenStreetMapPOIAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('localizedopenstreetmappoi'))
        return qs

class PendingModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'new_values', 'created', 'modified')
    ordering = ('target_object_class', 'target_object_id', )
    search_fields = ('target_object_class', 'target_object_id', 'action', )
    readonly_fields = ('target_object_link', 'created', 'modified')
    fieldsets = [
        (None, {'fields': ['created', 'modified']}),
        (u'Target object', {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (u'Modification', {'fields': ['action', 'new_values', 'apply']}),
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
                None
    
    actions=[apply_modification]

class ArchivedModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'new_values', 'created', 'modified')
    ordering = ('target_object_class', 'target_object_id', )
    search_fields = ('target_object_class', 'target_object_id', 'action', )
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

admin.site.register(Language, LanguageAdmin)
admin.site.register(OpenStreetMapPOI, OpenStreetMapPOIAdmin)
admin.site.register(PendingModification, PendingModificationAdmin)
admin.site.register(ArchivedModification, ArchivedModificationAdmin)
