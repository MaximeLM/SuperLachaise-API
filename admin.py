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

import datetime, traceback, sys, urllib
from django.contrib import admin, messages
import django.core.management
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.utils import timezone, translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class AdminUtils():
    
    @classmethod
    def change_page_url(cls, object):
        """ Return the URL for the change page of an object """
        if object and object.pk:
            app_name = object._meta.app_label
            reverse_name = object.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(object.pk,))
            return url
    
    @classmethod
    def changelist_page_url(cls, model):
        """ Return the URL for the changelist page of a model """
        app_name = model._meta.app_label
        reverse_name = model.__name__.lower()
        reverse_path = "admin:%s_%s_changelist" % (app_name, reverse_name)
        url = reverse(reverse_path)
        return url
    
    EXECUTE_SYNC_DONE_FORMAT = _('{synchronization_name}: done')
    EXECUTE_SYNC_ERROR_FORMAT = _('{synchronization_name}: {error}')
    
    @classmethod
    def execute_sync(cls, synchronization_name, request, args={}):
        """ Execute a synchronisation and add success/error messages to the request """
        try:
            sync_start = timezone.now()
            django.core.management.call_command(Synchronization.PREFIX + synchronization_name, **args)
            
            messages.success(request, cls.EXECUTE_SYNC_DONE_FORMAT.format(synchronization_name=synchronization_name))
        except:
            messages.error(request, cls.EXECUTE_SYNC_ERROR_FORMAT.format(synchronization_name=synchronization_name, error=sys.exc_info()[1]))
    
    @classmethod
    def current_localization(cls, object):
        """ Return the localized object for the current language if it exists """
        
        # Get current language
        language = Language.objects.filter(code=translation.get_language().split("-", 1)[0]).first()
        
        if language:
            return object.localizations.filter(language=language).first()
    
    @classmethod
    def delete_notes(cls, queryset):
        """ Empty the notes field of all objects in a queryset """
        queryset.update(notes=u'')
    
    HTML_LINK_FORMAT = u"<a href='{url}'>{name}</a>"
    
    @classmethod
    def html_link(cls, url, name=None):
        """ Return an HTML <a> tag for an URL and optional name (defaults to the URL) """
        if url:
            return mark_safe(cls.HTML_LINK_FORMAT.format(url=url.replace("'","%27"), name=name if name else url))
    
    HTML_IMAGE_LINK_FORMAT = u'<div style="background: url({image_url}); width:{width}px; height:{height}px; background-position:center; background-size:cover;"><a href="{url}"><img width={width}px height={height}px/></a></div>'
    
    @classmethod
    def html_image_link(cls, url, image_url=None, width=150, height=150):
        """ Return an HTML link for an URL with an  image """
        if url:
            return mark_safe(cls.HTML_IMAGE_LINK_FORMAT.format(url=url.replace("'","%27"), image_url=image_url.replace("'","%27") if image_url else url.replace("'","%27"), width=width, height=height))
    
    DATE_WITH_ACCURACY_FORMAT = u'{date} ({accuracy})'
    DATE_WITHOUT_ACCURACY_FORMAT = u'{date}'
    
    @classmethod
    def date_with_accuracy(cls, date, accuracy):
        if date:
            if accuracy:
                return cls.DATE_WITH_ACCURACY_FORMAT.format(date=date, accuracy=accuracy)
            else:
                return cls.DATE_WITHOUT_ACCURACY_FORMAT.format(date=date)
    
    @classmethod
    def name_with_bold_first_letter_of_sorting_name(cls, name, sorting_name):
        if name:
            result = name
            if sorting_name:
                last_occurence = name.rfind(sorting_name.split(',')[0])
                if not last_occurence == -1:
                    result = name[:last_occurence] + u'<b>%s</b>' % (name[last_occurence]) + name[last_occurence+1:]
            
            return mark_safe(result)

class LocalizedSynchronizationInline(admin.StackedInline):
    model = LocalizedSynchronization
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'description', 'created', 'modified']}),
    ]
    readonly_fields = ('created', 'modified')

@admin.register(Synchronization)
class SynchronizationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'dependency_order', 'last_executed', 'created_objects', 'modified_objects', 'deleted_objects', 'errors', 'description', 'notes')
    search_fields = ('name', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'dependency_order', 'last_executed', 'created_objects', 'modified_objects', 'deleted_objects', 'errors']}),
    ]
    readonly_fields = ('description', 'created', 'modified')
    
    inlines = [
        LocalizedSynchronizationInline,
    ]
    
    def description(self, obj):
        current_localization = AdminUtils.current_localization(obj)
        if current_localization:
            return current_localization.description
    description.short_description = _('description')
    
    def perform_commands(self, request, queryset):
        for synchronization in queryset.order_by('dependency_order'):
            AdminUtils.execute_sync(synchronization.name, request)
    perform_commands.short_description = _('Execute selected admin commands')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, perform_commands]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code', 'description', 'enumeration_separator', 'last_enumeration_separator', 'artist_prefix', 'notes')
    search_fields = ('code', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['code', 'description', 'enumeration_separator', 'last_enumeration_separator', 'artist_prefix']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

class LocalizedSettingInline(admin.StackedInline):
    model = LocalizedSetting
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'description', 'created', 'modified']}),
    ]
    readonly_fields = ('created', 'modified')

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'key', 'value', 'default', 'description', 'notes')
    search_fields = ('key', 'value', 'default', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['key', 'value', 'default']}),
    ]
    readonly_fields = ('description', 'created', 'modified')
    
    inlines = [
        LocalizedSettingInline,
    ]
    
    def description(self, obj):
        current_localization = AdminUtils.current_localization(obj)
        if current_localization:
            return current_localization.description
    description.short_description = _('description')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(OpenStreetMapElement)
class OpenStreetMapElementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'deleted', 'name', 'sorting_name', 'openstreetmap_id', 'type', 'openstreetmap_link', 'wikidata_links', 'wikimedia_commons_link', 'latitude', 'longitude', 'modified', 'notes')
    list_filter = ('type', 'nature', 'deleted',)
    search_fields = ('name', 'openstreetmap_id', 'wikidata', 'wikimedia_commons', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['deleted', 'name', 'sorting_name', 'openstreetmap_id', 'type', 'nature', 'latitude', 'longitude', 'wikidata', 'wikidata_links', 'wikimedia_commons', 'wikimedia_commons_link']}),
    ]
    readonly_fields = ('created', 'modified', 'openstreetmap_link', 'wikidata_links', 'wikimedia_commons_link')
    
    def openstreetmap_link(self, obj):
        return AdminUtils.html_link(obj.openstreetmap_url())
    openstreetmap_link.allow_tags = True
    openstreetmap_link.short_description = _('openstreetmap')
    
    def wikidata_links(self, obj):
        if obj.wikidata:
            language_code = translation.get_language().split("-", 1)[0]
            return ';'.join([AdminUtils.html_link(obj.wikidata_url(language_code, wikidata), wikidata) for wikidata in obj.wikidata_list()])
    wikidata_links.allow_tags = True
    wikidata_links.short_description = _('wikidata')
    wikidata_links.admin_order_field = 'wikidata'
    
    def wikimedia_commons_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_url(), obj.wikimedia_commons)
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons'
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

class WikidataLocalizedEntryInline(admin.StackedInline):
    model = WikidataLocalizedEntry
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'name', 'wikipedia', 'wikipedia_link', 'description']}),
    ]
    readonly_fields = ('wikipedia_link',)
    
    def wikipedia_link(self, obj):
        return AdminUtils.html_link(obj.wikipedia_url(), obj.wikipedia)
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'

@admin.register(WikidataEntry)
class WikidataEntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'deleted', 'name', 'wikidata_link', 'instance_of_link', 'sex_or_gender_link', 'occupations_link', 'grave_of_wikidata_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'burial_plot_reference', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'modified', 'notes')
    list_filter = ('deleted',)
    search_fields = ('localizations__name', 'wikidata_id', 'instance_of', 'sex_or_gender', 'occupations', 'wikimedia_commons_category', 'wikimedia_commons_grave_category', 'grave_of_wikidata', 'burial_plot_reference', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['deleted', 'wikidata_id', 'wikidata_link', 'instance_of', 'instance_of_link', 'sex_or_gender', 'sex_or_gender_link', 'occupations', 'occupations_link', 'grave_of_wikidata', 'grave_of_wikidata_link', 'wikimedia_commons_category', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category', 'wikimedia_commons_grave_category_link', 'burial_plot_reference', 'date_of_birth', 'date_of_birth_accuracy', 'date_of_death', 'date_of_death_accuracy']}),
    ]
    readonly_fields = ('name', 'wikidata_link', 'instance_of_link', 'sex_or_gender_link', 'occupations_link', 'grave_of_wikidata_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'created', 'modified')
    
    inlines = [
        WikidataLocalizedEntryInline,
    ]
    
    def name(self, obj):
        current_localization = AdminUtils.current_localization(obj)
        if current_localization:
            return current_localization.name
    name.short_description = _('name')
    
    def wikidata_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        return AdminUtils.html_link(obj.wikidata_url(language_code, obj.wikidata_id), obj.wikidata_id)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_id'
    
    def instance_of_link(self, obj):
        if obj.instance_of:
            language_code = translation.get_language().split("-", 1)[0]
            return ';'.join([AdminUtils.html_link(obj.wikidata_url(language_code, wikidata), wikidata) for wikidata in obj.wikidata_list("instance_of")])
    instance_of_link.allow_tags = True
    instance_of_link.short_description = _('instance of')
    instance_of_link.admin_order_field = 'instance_of'
    
    def occupations_link(self, obj):
        if obj.occupations:
            language_code = translation.get_language().split("-", 1)[0]
            return ';'.join([AdminUtils.html_link(obj.wikidata_url(language_code, wikidata), wikidata) for wikidata in obj.wikidata_list("occupations")])
    occupations_link.allow_tags = True
    occupations_link.short_description = _('occupations')
    occupations_link.admin_order_field = 'occupations'
    
    def sex_or_gender_link(self, obj):
        if obj.sex_or_gender:
            language_code = translation.get_language().split("-", 1)[0]
            return ';'.join([AdminUtils.html_link(obj.wikidata_url(language_code, wikidata), wikidata) for wikidata in obj.wikidata_list("sex_or_gender")])
    sex_or_gender_link.allow_tags = True
    sex_or_gender_link.short_description = _('sex or gender')
    sex_or_gender_link.admin_order_field = 'sex_or_gender'
    
    def grave_of_wikidata_link(self, obj):
        if obj.grave_of_wikidata:
            language_code = translation.get_language().split("-", 1)[0]
            return ';'.join([AdminUtils.html_link(obj.wikidata_url(language_code, wikidata), wikidata) for wikidata in obj.wikidata_list("grave_of_wikidata")])
    grave_of_wikidata_link.allow_tags = True
    grave_of_wikidata_link.short_description = _('grave_of:wikidata')
    grave_of_wikidata_link.admin_order_field = 'grave_of_wikidata'
    
    def wikimedia_commons_category_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_category_url("wikimedia_commons_category"), obj.wikimedia_commons_category)
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def wikimedia_commons_grave_category_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_category_url("wikimedia_commons_grave_category"), obj.wikimedia_commons_category)
    wikimedia_commons_grave_category_link.allow_tags = True
    wikimedia_commons_grave_category_link.short_description = _('wikimedia commons grave category')
    wikimedia_commons_grave_category_link.admin_order_field = 'wikimedia_commons_grave_category'
    
    def date_of_birth_with_accuracy(self, obj):
        return AdminUtils.date_with_accuracy(obj.date_of_birth, obj.date_of_birth_accuracy)
    date_of_birth_with_accuracy.short_description = _('date of birth')
    date_of_birth_with_accuracy.admin_order_field = 'date_of_birth'
    
    def date_of_death_with_accuracy(self, obj):
        return AdminUtils.date_with_accuracy(obj.date_of_death, obj.date_of_death_accuracy)
    date_of_death_with_accuracy.short_description = _('date of death')
    date_of_death_with_accuracy.admin_order_field = 'date_of_death'
    
    def sync_entry(self, request, queryset):
        wikidata_ids = [wikidata_entry.wikidata_id for wikidata_entry in queryset]
        return AdminUtils.execute_sync('wikidata', request, {"wikidata_ids": '|'.join(wikidata_ids)})
    sync_entry.short_description = _('Sync selected wikidata entries')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, sync_entry]

@admin.register(WikidataLocalizedEntry)
class WikidataLocalizedEntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_entry_link', 'language', 'name', 'wikidata_link', 'wikipedia_link', 'description', 'modified', 'notes')
    list_filter = ('language',)
    search_fields = ('name', 'wikidata_entry__id', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_entry', 'language', 'name', 'wikipedia', 'wikidata_link', 'wikipedia_link', 'description']}),
    ]
    readonly_fields = ('wikidata_entry_link', 'wikidata_link', 'wikipedia_link', 'created', 'modified')
    
    def wikidata_entry_link(self, obj):
        return AdminUtils.html_link(AdminUtils.change_page_url(obj.wikidata_entry), unicode(obj.wikidata_entry))
    wikidata_entry_link.allow_tags = True
    wikidata_entry_link.short_description = _('wikidata entry')
    wikidata_entry_link.admin_order_field = 'wikidata_entry'
    
    def wikidata_link(self, obj):
        if obj.wikidata_entry:
            language_code = translation.get_language().split("-", 1)[0]
            return AdminUtils.html_link(obj.wikidata_entry.wikidata_url(language_code, obj.wikidata_entry.wikidata_id), obj.wikidata_entry.wikidata_id)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_entry'
    
    def wikipedia_link(self, obj):
        return AdminUtils.html_link(obj.wikipedia_url(), obj.wikipedia)
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def sync_entry(self, request, queryset):
        wikidata_ids = [wikidata_localized_entry.wikidata_entry.wikidata_id for wikidata_localized_entry in queryset]
        return AdminUtils.execute_sync('wikidata', request, {"wikidata_ids": '|'.join(wikidata_ids)})
    sync_entry.short_description = _('Sync selected localized wikidata entries')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_entry]

@admin.register(WikipediaPage)
class WikipediaPageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_localized_entry_link', 'wikipedia_link', 'title', 'default_sort', 'intro_html', 'modified', 'notes')
    list_filter = ('wikidata_localized_entry__language',)
    search_fields = ('wikidata_localized_entry__name', 'wikidata_localized_entry__wikipedia', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_localized_entry', 'wikipedia_link', 'title', 'default_sort', 'intro', 'intro_html']}),
    ]
    readonly_fields = ('wikidata_localized_entry_link', 'wikipedia_link', 'intro_html', 'created', 'modified')
    
    def wikidata_localized_entry_link(self, obj):
        return AdminUtils.html_link(AdminUtils.change_page_url(obj.wikidata_localized_entry), unicode(obj.wikidata_localized_entry))
    wikidata_localized_entry_link.allow_tags = True
    wikidata_localized_entry_link.short_description = _('wikidata localized entry')
    wikidata_localized_entry_link.admin_order_field = 'wikidata_localized_entry'
    
    def wikipedia_link(self, obj):
        return AdminUtils.html_link(obj.wikidata_localized_entry.wikipedia_url(), obj.wikidata_localized_entry.wikipedia)
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def intro_html(self, obj):
        return obj.intro
    intro_html.allow_tags = True
    intro_html.short_description = _('intro')
    intro_html.admin_order_field = 'intro'
    
    def sync_entry(self, request, queryset):
        wikidata_localized_entry_ids = [str(value) for value in queryset.values_list('wikidata_localized_entry_id', flat=True)]
        return AdminUtils.execute_sync('wikipedia', request, {"wikidata_localized_entry_ids": '|'.join(wikidata_localized_entry_ids)})
    sync_entry.short_description = _('Sync selected wikipedia pages')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_entry]

@admin.register(WikimediaCommonsCategory)
class WikimediaCommonsCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'deleted', 'wikimedia_commons_link', 'main_image_link', 'category_members_link', 'modified', 'notes')
    list_filter = ('deleted',)
    search_fields = ('wikimedia_commons_id', 'main_image', 'category_members', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['deleted', 'wikimedia_commons_id', 'wikimedia_commons_link', 'main_image', 'main_image_link', 'category_members', 'category_members_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'main_image_link', 'category_members_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_url(obj.wikimedia_commons_id), obj.wikimedia_commons_id)
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons_id'
    
    def main_image_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_url(obj.main_image), obj.main_image)
    main_image_link.allow_tags = True
    main_image_link.short_description = _('main image')
    main_image_link.admin_order_field = 'main_image'
    
    def category_members_link(self, obj):
        if obj.category_members:
            return '|'.join([AdminUtils.html_link(obj.wikimedia_commons_url(category_member), category_member) for category_member in obj.category_members_list()])
    category_members_link.allow_tags = True
    category_members_link.short_description = _('category members')
    category_members_link.admin_order_field = 'category_members'
    
    def sync_object(self, request, queryset):
        wikimedia_commons_categories = [wikimedia_commons_category.wikimedia_commons_id for wikimedia_commons_category in queryset]
        return AdminUtils.execute_sync('wikimedia_commons_categories', request, {"wikimedia_commons_categories": '|'.join(wikimedia_commons_categories)})
    sync_object.short_description = _('Sync selected wikimedia commons categories')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_object]

@admin.register(WikimediaCommonsFile)
class WikimediaCommonsFileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'modified', 'notes')
    search_fields = ('wikimedia_commons_id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikimedia_commons_id', 'wikimedia_commons_link', 'original_url', 'original_url_link', 'thumbnail_url', 'thumbnail_url_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        return AdminUtils.html_link(obj.wikimedia_commons_url(), obj.wikimedia_commons_id)
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons_id'
    
    def original_url_link(self, obj):
        return AdminUtils.html_link(obj.original_url, _('original image'))
    original_url_link.allow_tags = True
    original_url_link.short_description = _('original url')
    original_url_link.admin_order_field = 'original_url'
    
    def thumbnail_url_link(self, obj):
        return AdminUtils.html_image_link(obj.thumbnail_url)
    thumbnail_url_link.allow_tags = True
    thumbnail_url_link.short_description = _('thumbnail url')
    thumbnail_url_link.admin_order_field = 'thumbnail_url'
    
    def sync_object(self, request, queryset):
        wikimedia_commons_files = [wikimedia_commons_file.wikimedia_commons_id for wikimedia_commons_file in queryset]
        return AdminUtils.execute_sync('wikimedia_commons_files', request, {"wikimedia_commons_files": '|'.join(wikimedia_commons_files)})
    sync_object.short_description = _('Sync selected wikimedia commons files')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_object]

class SuperLachaiseLocalizedPOIInline(admin.StackedInline):
    model = SuperLachaiseLocalizedPOI
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'name', 'sorting_name', 'description', 'created', 'modified']}),
    ]
    readonly_fields = ('created', 'modified')

class SuperLachaiseWikidataRelationInline(admin.StackedInline):
    model = SuperLachaisePOI.wikidata_entries.through
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['wikidata_entry', 'name', 'relation_type']}),
    ]
    readonly_fields = ('name',)
    
    def name(self, obj):
        current_localization = AdminUtils.current_localization(obj.wikidata_entry)
        if current_localization:
            return current_localization.name
    name.short_description = _('name')
    
    verbose_name = "wikidata entry"
    verbose_name_plural = "wikidata entries"

class SuperLachaiseCategoryRelationInline(admin.StackedInline):
    model = SuperLachaiseCategoryRelation
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['superlachaise_category']}),
    ]
    
    verbose_name = "superlachaise category"
    verbose_name_plural = "superlachaise categories"

@admin.register(SuperLachaisePOI)
class SuperLachaisePOIAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pk', 'deleted', 'openstreetmap_element_link', 'wikidata_entries_link', 'superlachaise_categories_link', 'burial_plot_reference', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'wikimedia_commons_category_link', 'main_image_link', 'modified', 'notes')
    list_filter = ('superlachaise_categories', 'deleted',)
    search_fields = ('openstreetmap_element__name', 'wikidata_entries__id', 'wikidata_entries__localizations__name', 'burial_plot_reference', 'wikimedia_commons_category__id', 'main_image__id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['deleted', 'pk', 'openstreetmap_element', 'burial_plot_reference', 'date_of_birth', 'date_of_birth_accuracy', 'date_of_death', 'date_of_death_accuracy', 'wikimedia_commons_category', 'main_image']}),
    ]
    readonly_fields = ('pk', 'openstreetmap_element_link', 'wikidata_entries_link', 'superlachaise_categories_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'wikimedia_commons_category_link', 'main_image_link', 'created', 'modified')
    
    inlines = [
        SuperLachaiseLocalizedPOIInline,
        SuperLachaiseWikidataRelationInline,
        SuperLachaiseCategoryRelationInline,
    ]
    
    def openstreetmap_element_link(self, obj):
        return AdminUtils.html_link(AdminUtils.change_page_url(obj.openstreetmap_element), unicode(obj.openstreetmap_element))
    openstreetmap_element_link.allow_tags = True
    openstreetmap_element_link.short_description = _('openstreetmap element')
    openstreetmap_element_link.admin_order_field = 'openstreetmap_element'
    
    def wikidata_entries_link(self, obj):
        return ';'.join([AdminUtils.html_link(AdminUtils.change_page_url(wikidata_entry_relation.wikidata_entry), wikidata_entry_relation.relation_type + u':' + unicode(wikidata_entry_relation.wikidata_entry)) for wikidata_entry_relation in obj.superlachaisewikidatarelation_set.all()])
    wikidata_entries_link.allow_tags = True
    wikidata_entries_link.short_description = _('wikidata entries')
    wikidata_entries_link.admin_order_field = 'wikidata_entries'
    
    def superlachaise_categories_link(self, obj):
        return ';'.join([AdminUtils.html_link(AdminUtils.change_page_url(superlachaise_category), unicode(superlachaise_category)) for superlachaise_category in obj.superlachaise_categories.all()])
    superlachaise_categories_link.allow_tags = True
    superlachaise_categories_link.short_description = _('superlachaise categories')
    superlachaise_categories_link.admin_order_field = 'superlachaise_categories'
    
    def date_of_birth_with_accuracy(self, obj):
        return AdminUtils.date_with_accuracy(obj.date_of_birth, obj.date_of_birth_accuracy)
    date_of_birth_with_accuracy.short_description = _('date of birth')
    date_of_birth_with_accuracy.admin_order_field = 'date_of_birth'
    
    def date_of_death_with_accuracy(self, obj):
        return AdminUtils.date_with_accuracy(obj.date_of_death, obj.date_of_death_accuracy)
    date_of_death_with_accuracy.short_description = _('date of death')
    date_of_death_with_accuracy.admin_order_field = 'date_of_death'
    
    def wikimedia_commons_category_link(self, obj):
        return AdminUtils.html_link(AdminUtils.change_page_url(obj.wikimedia_commons_category), unicode(obj.wikimedia_commons_category))
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def main_image_link(self, obj):
        if obj.main_image:
            return AdminUtils.html_image_link(AdminUtils.change_page_url(obj.main_image), obj.main_image.thumbnail_url)
    main_image_link.allow_tags = True
    main_image_link.short_description = _('main image')
    main_image_link.admin_order_field = 'main_image'
    
    def sync_object(self, request, queryset):
        openstreetmap_element_ids = [superlachaise_poi.openstreetmap_element.openstreetmap_id for superlachaise_poi in queryset]
        return AdminUtils.execute_sync('superlachaise_pois', request, {"openstreetmap_element_ids": '|'.join(openstreetmap_element_ids)})
    sync_object.short_description = _('Sync selected superlachaise POIs')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_object]

@admin.register(SuperLachaiseLocalizedPOI)
class SuperLachaiseLocalizedPOIAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'superlachaise_poi_link', 'language', 'name_with_bold', 'sorting_name', 'description', 'modified', 'notes')
    list_filter = ('language',)
    search_fields = ('name', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['superlachaise_poi', 'language', 'name', 'sorting_name', 'description']}),
    ]
    readonly_fields = ('superlachaise_poi_link', 'name_with_bold', 'created', 'modified')
    
    def superlachaise_poi_link(self, obj):
        return AdminUtils.html_link(AdminUtils.change_page_url(obj.superlachaise_poi), unicode(obj.superlachaise_poi))
    superlachaise_poi_link.allow_tags = True
    superlachaise_poi_link.short_description = _('superlachaise poi')
    superlachaise_poi_link.admin_order_field = 'superlachaise_poi'
    
    def name_with_bold(self, obj):
        return AdminUtils.name_with_bold_first_letter_of_sorting_name(obj.name, obj.sorting_name)
    name_with_bold.allow_tags = True
    name_with_bold.short_description = _('name')
    name_with_bold.admin_order_field = 'name'
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    def sync_object(self, request, queryset):
        openstreetmap_element_ids = [superlachaise_localized_poi.superlachaise_poi.openstreetmap_element.openstreetmap_id for superlachaise_localized_poi in queryset]
        return AdminUtils.execute_sync('superlachaise_pois', {"openstreetmap_element_ids": '|'.join(openstreetmap_element_ids)}, request)
    sync_object.short_description = _('Sync selected superlachaise localized POIs')
    
    actions = [delete_notes, sync_object]

class SuperLachaiseLocalizedCategoryInline(admin.StackedInline):
    model = SuperLachaiseLocalizedCategory
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'name']}),
    ]

@admin.register(SuperLachaiseCategory)
class SuperLachaiseCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'deleted', 'code', 'type', 'values', 'members_count', 'wikidata_occupations_count', 'modified', 'notes')
    list_filter = ('type', 'deleted',)
    search_fields = ('code', 'type', 'values', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['deleted', 'code', 'type', 'values']}),
    ]
    readonly_fields = ('code', 'members_count', 'wikidata_occupations_count', 'created', 'modified')
    inlines = [
        SuperLachaiseLocalizedCategoryInline,
    ]
    
    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = _('members count')
    
    def wikidata_occupations_count(self, obj):
        return obj.wikidata_occupations.count()
    wikidata_occupations_count.short_description = _('wikidata occupations count')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(WikidataOccupation)
class WikidataOccupationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_link', 'name', 'superlachaise_category', 'used_in_link', 'modified', 'notes')
    list_filter = ('superlachaise_category',)
    list_editable = ('superlachaise_category',)
    search_fields = ('wikidata_id', 'name', 'used_in__id', 'used_in__localizations__name', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_id', 'wikidata_link', 'name', 'superlachaise_category', 'used_in']}),
    ]
    filter_horizontal = ('used_in',)
    readonly_fields = ('wikidata_link', 'used_in_link', 'created', 'modified')
    
    def wikidata_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        return AdminUtils.html_link(obj.wikidata_url(language_code), obj.wikidata_id)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_id'
    
    def used_in_count(self, obj):
        return obj.used_in.count()
    used_in_count.short_description = _('used in count')
    
    def used_in_link(self, obj):
        return ';'.join([AdminUtils.html_link(AdminUtils.change_page_url(wikidata_entry), unicode(wikidata_entry)) for wikidata_entry in obj.used_in.all()])
    used_in_link.allow_tags = True
    used_in_link.short_description = _('used in')
    used_in_link.admin_order_field = 'used_in'
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(DBVersion)
class DBVersionAdmin(admin.ModelAdmin):
    list_display = ('version_id', 'modified', 'notes')
    search_fields = ('version_id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['version_id']}),
    ]
    readonly_fields = ('created', 'modified')
    
    def create_db_version(self, request, queryset):
        django.core.management.call_command("create_db_version")
    create_db_version.short_description = _('Create DB version')
    
    def delete_notes(self, request, queryset):
        AdminUtils.delete_notes(queryset)
    delete_notes.short_description = _('Delete notes')
    
    actions=[create_db_version, delete_notes]
