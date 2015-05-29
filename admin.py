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

import urllib
from django.contrib import admin
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class AdminCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_executed', 'last_result', 'description', 'notes')
    search_fields = ('name', 'description',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'last_executed', 'last_result', 'description']}),
    ]
    readonly_fields = ('last_executed', 'last_result', 'created', 'modified')
    
    def perform_commands(self, request, queryset):
        for admin_command in queryset:
            try:
                admin_command.perform_command()
            except Exception as exception:
                print exception
    perform_commands.short_description = _('Execute selected admin commands')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions=[delete_notes, perform_commands]

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'notes')
    search_fields = ('code', 'description',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['code', 'description']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions = [delete_notes]

class OpenStreetMapElementAdmin(admin.ModelAdmin):
    list_display = ('sorted_name', 'type', 'openstreetmap_link', 'wikipedia_link', 'wikidata_link', 'subject_wikipedia_link', 'wikimedia_commons_link', 'latitude', 'longitude', 'notes')
    search_fields = ('name', 'type', 'id', 'wikidata', 'wikimedia_commons',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'sorting_name', 'type', 'id', 'latitude', 'longitude']}),
        (_('Tags'), {'fields': ['wikipedia', 'wikidata', 'subject_wikipedia', 'wikimedia_commons']}),
    ]
    readonly_fields = ('sorted_name', 'created', 'modified', 'openstreetmap_link', 'wikipedia_link', 'wikidata_link', 'subject_wikipedia_link', 'wikimedia_commons_link')
    
    def sorted_name(self, obj):
        return obj.name
    sorted_name.short_description = _('name')
    sorted_name.admin_order_field = 'sorting_name'
    
    def openstreetmap_link(self, obj):
        url = u'https://www.openstreetmap.org/{type}/{id}'.format(type=obj.type, id=unicode(obj.id))
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
    openstreetmap_link.allow_tags = True
    openstreetmap_link.short_description = _('OpenStreetMap')
    openstreetmap_link.admin_order_field = 'id'
    
    def wikipedia_link(self, obj):
        if obj.wikipedia:
            language = obj.wikipedia.split(':')[0]
            
            result = []
            for link in obj.wikipedia.split(':')[1].split(';'):
                url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=language, name=unicode(link)).replace("'","%27")
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return language + ':' + ';'.join(result)
        else:
            return None
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def wikidata_link(self, obj):
        if obj.wikidata:
            language = translation.get_language().split("-", 1)[0]
            
            result = []
            for link in obj.wikidata.split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
        else:
            return None
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata'
    
    def subject_wikipedia_link(self, obj):
        if obj.subject_wikipedia:
            language = obj.subject_wikipedia.split(':')[0]
            
            result = []
            for link in obj.subject_wikipedia.split(':')[1].split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return language + ':' + ';'.join(result)
        else:
            return None
    subject_wikipedia_link.allow_tags = True
    subject_wikipedia_link.short_description = _('subject:wikipedia')
    subject_wikipedia_link.admin_order_field = 'subject_wikipedia'
    
    def wikimedia_commons_link(self, obj):
        if obj.wikimedia_commons:
            url = u'http://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons)))
        else:
            return None
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions = [delete_notes]

class PendingModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'modified_fields', 'notes')
    ordering = ('action', 'target_object_class', 'target_object_id',)
    search_fields = ('target_object_class', 'target_object_id', 'action', 'modified_fields',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (_('Target object'), {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (_('Modification'), {'fields': ['action', 'modified_fields']}),
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
            return _('None')
    target_object_link.allow_tags = True
    target_object_link.short_description = _('target object link')
    
    def apply_modifications(self, request, queryset):
        for pending_modification in queryset:
            try:
                pending_modification.apply_modification()
            except Exception as exception:
                print exception
    apply_modifications.short_description = _('Apply selected pending modifications')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions=[delete_notes, apply_modifications]

class SettingAdmin(admin.ModelAdmin):
    list_display = ('category', 'key', 'value', 'description', 'notes')
    search_fields = ('category', 'key', 'value', 'description',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['category', 'key', 'value', 'description']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions = [delete_notes]

class WikidataEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'wikidata_link', 'instance_of_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'notes')
    search_fields = ('id', 'wikimedia_commons_category', 'wikimedia_commons_grave_category',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['id', 'instance_of', 'wikimedia_commons_category', 'wikimedia_commons_grave_category']}),
        (_('Dates'), {'fields': ['date_of_birth', 'date_of_birth_accuracy', 'date_of_death', 'date_of_death_accuracy']}),
    ]
    readonly_fields = ('wikidata_link', 'instance_of_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'created', 'modified')
    
    def wikidata_link(self, obj):
        if obj.id:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.id), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
        else:
            return None
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'id'
    
    def instance_of_link(self, obj):
        if obj.instance_of:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.instance_of), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.instance_of)))
        else:
            return None
    instance_of_link.allow_tags = True
    instance_of_link.short_description = _('instance_of')
    instance_of_link.admin_order_field = 'instance_of'
    
    def wikimedia_commons_category_link(self, obj):
        if obj.wikimedia_commons_category:
            url = u'http://commons.wikimedia.org/wiki/Category:{name}'.format(name=unicode(obj.wikimedia_commons_category)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_category)))
        else:
            return None
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def wikimedia_commons_grave_category_link(self, obj):
        if obj.wikimedia_commons_grave_category:
            url = u'http://commons.wikimedia.org/wiki/Category:{name}'.format(name=unicode(obj.wikimedia_commons_grave_category)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_grave_category)))
        else:
            return None
    wikimedia_commons_grave_category_link.allow_tags = True
    wikimedia_commons_grave_category_link.short_description = _('wikimedia commons grave category')
    wikimedia_commons_grave_category_link.admin_order_field = 'wikimedia_commons_grave_category'
    
    def date_of_birth_with_accuracy(self, obj):
        date = obj.date_of_birth if obj.date_of_birth else u''
        accuracy = u' (%s)' % obj.date_of_birth_accuracy if obj.date_of_birth_accuracy else u''
        return u'{date}{accuracy}'.format(accuracy=accuracy, date=date)
    date_of_birth_with_accuracy.short_description = _('date of birth')
    date_of_birth_with_accuracy.admin_order_field = 'date_of_birth'
    
    def date_of_death_with_accuracy(self, obj):
        date = obj.date_of_death if obj.date_of_death else u''
        accuracy = u' (%s)' % obj.date_of_death_accuracy if obj.date_of_death_accuracy else u''
        return u'{date}{accuracy}'.format(accuracy=accuracy, date=date)
    date_of_death_with_accuracy.short_description = _('date of death')
    date_of_death_with_accuracy.admin_order_field = 'date_of_death'
    
    def sync_entry(self, request, queryset):
        wikidata_ids = []
        for wikidata_entry in queryset:
            wikidata_ids.append(str(wikidata_entry.id))
        call_command('sync_wikidata', wikidata_ids='|'.join(wikidata_ids))
    sync_entry.short_description = _('Sync selected wikidata entries')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions=[delete_notes, sync_entry]

class LocalizedWikidataEntryAdmin(admin.ModelAdmin):
    list_display = ('language', 'wikidata_link', 'name', 'wikipedia_link', 'description', 'notes')
    search_fields = ('language', 'parent', 'name',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['language', 'parent']}),
        (None, {'fields': ['name', 'wikipedia', 'description']}),
    ]
    readonly_fields = ('wikidata_link', 'wikipedia_link', 'created', 'modified')
    
    def wikidata_link(self, obj):
        if obj.parent and obj.parent.id:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.parent.id), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.parent.id)))
        else:
            return None
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'parent'
    
    def wikipedia_link(self, obj):
        if obj.wikipedia:
            url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=obj.language.code, name=unicode(obj.wikipedia)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikipedia)))
        else:
            return None
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete selected objects notes')
    
    actions = [delete_notes]

admin.site.register(AdminCommand, AdminCommandAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(OpenStreetMapElement, OpenStreetMapElementAdmin)
admin.site.register(PendingModification, PendingModificationAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(WikidataEntry, WikidataEntryAdmin)
admin.site.register(LocalizedWikidataEntry, LocalizedWikidataEntryAdmin)
