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

import datetime
from django.contrib import admin
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone, translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

@admin.register(AdminCommand)
class AdminCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'dependency_order', 'last_executed', 'last_result', 'description', 'notes')
    search_fields = ('name', 'last_result', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'dependency_order', 'last_executed', 'last_result', 'description']}),
    ]
    readonly_fields = ('last_executed', 'last_result', 'created', 'modified')
    
    def perform_commands(self, request, queryset):
        for admin_command in queryset.order_by('dependency_order'):
            try:
                admin_command.perform_command()
            except Exception as exception:
                print exception
    perform_commands.short_description = _('Execute selected admin commands')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, perform_commands]

@admin.register(AdminCommandError)
class AdminCommandErrorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'admin_command_link', 'type', 'target_object_link', 'description', 'notes')
    list_filter = ('admin_command', 'type',)
    search_fields = ('target_object_class', 'target_object_id', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['admin_command', 'type', 'description']}),
        (_('Target object'), {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
    ]
    readonly_fields = ('admin_command_link', 'target_object_link', 'created', 'modified')
    
    def admin_command_link(self, obj):
        if obj.admin_command:
            app_name = obj._meta.app_label
            reverse_name = obj.admin_command.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.admin_command.id,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.admin_command)))
    admin_command_link.allow_tags = True
    admin_command_link.short_description = _('admin command')
    admin_command_link.admin_order_field = 'admin_command'
    
    def target_object_link(self, obj):
        if obj.target_object():
            app_name = obj._meta.app_label
            reverse_name = obj.target_object_class.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.target_object().id,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.target_object())))
    target_object_link.allow_tags = True
    target_object_link.short_description = _('target object')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'notes')
    search_fields = ('code', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['code', 'description']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(PendingModification)
class PendingModificationAdmin(admin.ModelAdmin):
    list_display = ('action', 'target_object_class', 'target_object_id', 'target_object_link', 'modified_fields', 'modified', 'notes')
    list_filter = ('action','target_object_class',)
    search_fields = ('target_object_id', 'modified_fields', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (_('Target object'), {'fields': ['target_object_class', 'target_object_id', 'target_object_link']}),
        (None, {'fields': ['action', 'modified_fields']}),
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
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, apply_modifications]

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('category', 'key', 'value', 'description', 'notes')
    list_filter = ('category',)
    search_fields = ('key', 'value', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['category', 'key', 'value', 'description']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(OpenStreetMapElement)
class OpenStreetMapElementAdmin(admin.ModelAdmin):
    list_display = ('sorted_name', 'openstreetmap_link', 'type', 'wikipedia_link', 'wikidata_link', 'wikidata_combined_link', 'wikimedia_commons_link', 'latitude', 'longitude', 'notes')
    search_fields = ('name', 'id', 'type', 'wikidata', 'wikipedia', 'wikimedia_commons', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'sorting_name', 'id', 'type', 'latitude', 'longitude', 'wikipedia', 'wikipedia_link', 'wikidata', 'wikidata_link', 'wikidata_combined', 'wikidata_combined_link', 'wikimedia_commons', 'wikimedia_commons_link']}),
    ]
    readonly_fields = ('sorted_name', 'created', 'modified', 'openstreetmap_link', 'wikipedia_link', 'wikidata_link', 'wikidata_combined_link', 'wikimedia_commons_link')
    
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
            result = []
            for link in obj.wikipedia.split(';'):
                if ':' in link:
                    language = link.split(':')[-2]
                    url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=language, name=unicode(link.split(':')[-1])).replace("'","%27")
                    result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
                else:
                    result.append(link)
            return ';'.join(result)
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def wikidata_link(self, obj):
        if obj.wikidata:
            language = translation.get_language().split("-", 1)[0]
            
            result = []
            for link in obj.wikidata.split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link.split(':')[-1]), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata'
    
    def wikidata_combined_link(self, obj):
        if obj.wikidata_combined:
            language = translation.get_language().split("-", 1)[0]
            
            result = []
            for link in obj.wikidata_combined.split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link.split(':')[-1]), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
    wikidata_combined_link.allow_tags = True
    wikidata_combined_link.short_description = _('wikidata combined')
    wikidata_combined_link.admin_order_field = 'wikidata_combined'
    
    def wikimedia_commons_link(self, obj):
        if obj.wikimedia_commons:
            url = u'http://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons)))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(WikidataEntry)
class WikidataEntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_link', 'instance_of_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'grave_of_wikidata_link', 'burial_plot_reference', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'notes')
    search_fields = ('wikidatalocalizedentry__name', 'id', 'wikimedia_commons_category', 'wikimedia_commons_grave_category', 'grave_of_wikidata', 'burial_plot_reference', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['id', 'wikidata_link', 'instance_of', 'instance_of_link', 'wikimedia_commons_category', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category', 'wikimedia_commons_grave_category_link', 'grave_of_wikidata', 'grave_of_wikidata_link', 'burial_plot_reference', 'date_of_birth', 'date_of_birth_accuracy', 'date_of_death', 'date_of_death_accuracy']}),
    ]
    readonly_fields = ('wikidata_link', 'instance_of_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'grave_of_wikidata_link', 'created', 'modified')
    
    def wikidata_link(self, obj):
        if obj.id:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.id), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'id'
    
    def instance_of_link(self, obj):
        if obj.instance_of:
            language = translation.get_language().split("-", 1)[0]
            
            result = []
            for link in obj.instance_of.split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
    instance_of_link.allow_tags = True
    instance_of_link.short_description = _('instance of')
    instance_of_link.admin_order_field = 'instance_of'
    
    def wikimedia_commons_category_link(self, obj):
        if obj.wikimedia_commons_category:
            url = u'http://commons.wikimedia.org/wiki/Category:{name}'.format(name=unicode(obj.wikimedia_commons_category)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_category)))
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def wikimedia_commons_grave_category_link(self, obj):
        if obj.wikimedia_commons_grave_category:
            url = u'http://commons.wikimedia.org/wiki/Category:{name}'.format(name=unicode(obj.wikimedia_commons_grave_category)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_grave_category)))
    wikimedia_commons_grave_category_link.allow_tags = True
    wikimedia_commons_grave_category_link.short_description = _('wikimedia commons grave category')
    wikimedia_commons_grave_category_link.admin_order_field = 'wikimedia_commons_grave_category'
    
    def grave_of_wikidata_link(self, obj):
        if obj.grave_of_wikidata:
            language = translation.get_language().split("-", 1)[0]
            
            result = []
            for link in obj.grave_of_wikidata.split(';'):
                url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(link), language=language)
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
    grave_of_wikidata_link.allow_tags = True
    grave_of_wikidata_link.short_description = _('grave_of:wikidata')
    grave_of_wikidata_link.admin_order_field = 'grave_of_wikidata'
    
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
        sync_start = timezone.now()
        call_command('sync_wikidata', wikidata_ids='|'.join(wikidata_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().id,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    
    sync_entry.short_description = _('Sync selected wikidata entries')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, sync_entry]

@admin.register(WikidataLocalizedEntry)
class WikidataLocalizedEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'wikidata_entry_link', 'wikidata_link', 'wikipedia_link', 'description', 'notes')
    list_filter = ('language',)
    search_fields = ('name', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['language', 'wikidata_entry', 'name', 'wikipedia', 'description']}),
    ]
    readonly_fields = ('wikidata_entry_link', 'wikidata_link', 'wikipedia_link', 'created', 'modified')
    
    def wikidata_entry_link(self, obj):
        if obj.wikidata_entry:
            app_name = obj._meta.app_label
            reverse_name = obj.wikidata_entry.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.wikidata_entry.id,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata_entry)))
    wikidata_entry_link.allow_tags = True
    wikidata_entry_link.short_description = _('wikidata entry')
    wikidata_entry_link.admin_order_field = 'wikidata_entry'
    
    def wikidata_link(self, obj):
        if obj.wikidata_entry:
            language = translation.get_language().split("-", 1)[0]
            url = u'http://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.wikidata_entry.id), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata_entry.id)))
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_entry'
    
    def wikipedia_link(self, obj):
        if obj.wikipedia:
            url = u'http://{language}.wikipedia.org/wiki/{name}'.format(language=obj.language.code, name=unicode(obj.wikipedia)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikipedia)))
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def sync_entry(self, request, queryset):
        wikidata_ids = []
        for wikidata_localized_entry in queryset:
            wikidata_ids.append(str(wikidata_localized_entry.wikidata_entry.id))
        sync_start = timezone.now()
        call_command('sync_wikidata', wikidata_ids='|'.join(wikidata_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().id,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_entry.short_description = _('Sync selected localized wikidata entries')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_entry]

@admin.register(WikipediaPage)
class WikipediaPageAdmin(admin.ModelAdmin):
    list_display = ('language', 'title_link', 'intro_html', 'notes')
    list_filter = ('language',)
    search_fields = ('title', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['language', 'title_link', 'intro', 'intro_html']}),
    ]
    readonly_fields = ('language', 'title', 'title_link', 'intro_html', 'created', 'modified')
    
    def title_link(self, obj):
        url = u'http://{language}.wikipedia.org/wiki/{title}'.format(language=obj.language.code, title=unicode(obj.title)).replace("'","%27")
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.title)))
    title_link.allow_tags = True
    title_link.short_description = _('wikipedia')
    title_link.admin_order_field = 'title'
    
    def intro_html(self, obj):
        return obj.intro
    intro_html.allow_tags = True
    intro_html.short_description = _('intro')
    intro_html.admin_order_field = 'intro'
    
    def sync_page(self, request, queryset):
        wikipedia_ids = []
        for wikipedia_page in queryset:
            wikipedia_ids.append(wikipedia_page.language.code + ':' + wikipedia_page.title)
        sync_start = timezone.now()
        call_command('sync_wikipedia', wikipedia_ids='|'.join(wikipedia_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().id,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_page.short_description = _('Sync selected wikipedia pages')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_page]

@admin.register(WikimediaCommonsCategory)
class WikimediaCommonsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'wikimedia_commons_link', 'files_link', 'main_image_link', 'notes')
    search_fields = ('id', 'files', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['id', 'wikimedia_commons_link', 'files', 'main_image', 'main_image_link', 'files_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'files_link', 'main_image_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        url = u'http://commons.wikimedia.org/wiki/Category:{name}'.format(name=unicode(obj.id)).replace("'","%27")
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons category')
    wikimedia_commons_link.admin_order_field = 'id'
    
    def files_link(self, obj):
        if obj.files:
            result = []
            for link in obj.files.split(';'):
                url = u'http://commons.wikimedia.org/wiki/{file}'.format(file=unicode(link).replace("'","%27"))
                result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(link))))
            return ';'.join(result)
    files_link.allow_tags = True
    files_link.short_description = _('files')
    files_link.admin_order_field = 'files'
    
    def main_image_link(self, obj):
        if obj.main_image:
            url = u'http://commons.wikimedia.org/wiki/{file}'.format(file=unicode(obj.main_image).replace("'","%27"))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.main_image)))
    main_image_link.allow_tags = True
    main_image_link.short_description = _('main image')
    main_image_link.admin_order_field = 'main_image'
    
    def sync_page(self, request, queryset):
        wikimedia_commons_categories = []
        for wikimedia_commons_category in queryset:
            wikimedia_commons_categories.append(wikimedia_commons_category.id)
        sync_start = timezone.now()
        call_command('sync_wikimedia_commons_categories', wikimedia_commons_categories='|'.join(wikimedia_commons_categories))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().id,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_page.short_description = _('Sync selected wikipedia pages')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_page]

@admin.register(WikimediaCommonsFile)
class WikimediaCommonsFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'notes')
    search_fields = ('id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['id', 'wikimedia_commons_link', 'original_url', 'original_url_link', 'thumbnail_url', 'thumbnail_url_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        url = u'http://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.id)).replace("'","%27")
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.id)))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons file')
    wikimedia_commons_link.admin_order_field = 'id'
    
    def original_url_link(self, obj):
        if obj.original_url:
            return mark_safe(u"<a href='%s'>%s</a>" % (obj.original_url, _('original image')))
    original_url_link.allow_tags = True
    original_url_link.short_description = _('original url')
    original_url_link.admin_order_field = 'original_url'
    
    def thumbnail_url_link(self, obj):
        if obj.thumbnail_url:
            thumbnail_width = u'350'
            display_size = u'350'
            result = """
            <div style="width:150px; height:150px; overflow:hidden;">
                <img src="{url}" style="width:400px; height:300px; margin: -75px 0 0 -100px;" />
            </div>
            """
            result = u'<div style="background: url({url}); width:150px; height:150px; background-position:center; background-size:cover;"><a href="{url}"><img width=150 height=150/></a></div>'.format(url=obj.thumbnail_url)
            return mark_safe(result)
    thumbnail_url_link.allow_tags = True
    thumbnail_url_link.short_description = _('thumbnail url')
    thumbnail_url_link.admin_order_field = 'thumbnail_url'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]
