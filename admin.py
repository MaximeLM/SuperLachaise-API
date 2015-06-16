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

import datetime, traceback, sys
from django.contrib import admin, messages
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.utils import timezone, translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from StringIO import StringIO

from superlachaise_api.models import *

def change_page_url(obj):
    app_name = obj._meta.app_label
    reverse_name = obj.__class__.__name__.lower()
    reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
    url = reverse(reverse_path, args=(obj.pk,))
    return url

class LocalizedAdminCommandInline(admin.StackedInline):
    model = LocalizedAdminCommand
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'description', 'created', 'modified']}),
    ]
    readonly_fields = ('created', 'modified')

@admin.register(AdminCommand)
class AdminCommandAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'dependency_order', 'last_executed', 'last_result', 'description', 'notes')
    search_fields = ('name', 'last_result', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'dependency_order', 'last_executed', 'last_result']}),
    ]
    readonly_fields = ('description', 'created', 'modified')
    
    inlines = [
        LocalizedAdminCommandInline,
    ]
    
    def description(self, obj):
        language = Language.objects.filter(code=translation.get_language().split("-", 1)[0]).first()
        localized_admin_command = None
        if language:
            localized_admin_command = obj.localizations.filter(language=language).first()
        if not localized_admin_command:
            localized_admin_command = obj.localizations.all().first()
        
        if localized_admin_command:
            return localized_admin_command.description
    description.short_description = _('description')
    
    def perform_commands(self, request, queryset):
        for admin_command in queryset.order_by('dependency_order'):
            try:
                admin_command.perform_command()
            except:
                messages.error(request, sys.exc_info()[1])
    perform_commands.short_description = _('Execute selected admin commands')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
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
        queryset.update(notes=u'')
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
    list_display = ('__unicode__', 'key', 'value', 'description', 'notes')
    search_fields = ('key', 'value', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['key', 'value']}),
    ]
    readonly_fields = ('description', 'created', 'modified')
    
    inlines = [
        LocalizedSettingInline,
    ]
    
    def description(self, obj):
        language = Language.objects.filter(code=translation.get_language().split("-", 1)[0]).first()
        localized_setting = None
        if language:
            localized_setting = obj.localizations.filter(language=language).first()
        if not localized_setting:
            localized_setting = obj.localizations.all().first()
        
        if localized_setting:
            return localized_setting.description
    description.short_description = _('description')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(OpenStreetMapElement)
class OpenStreetMapElementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'sorting_name', 'openstreetmap_id', 'type', 'openstreetmap_link', 'wikidata_links', 'wikimedia_commons_link', 'latitude', 'longitude', 'notes')
    list_filter = ('type', 'nature',)
    search_fields = ('name', 'openstreetmap_id', 'wikidata', 'wikimedia_commons', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['name', 'sorting_name', 'openstreetmap_id', 'type', 'nature', 'latitude', 'longitude', 'wikidata', 'wikidata_links', 'wikimedia_commons', 'wikimedia_commons_link']}),
    ]
    readonly_fields = ('created', 'modified', 'openstreetmap_link', 'wikidata_links', 'wikimedia_commons_link')
    
    def openstreetmap_link(self, obj):
        url = obj.openstreetmap_url()
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), unicode(url)))
    openstreetmap_link.allow_tags = True
    openstreetmap_link.short_description = _('openStreetMap')
    
    def wikidata_links(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code)
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    wikidata_links.allow_tags = True
    wikidata_links.short_description = _('wikidata')
    wikidata_links.admin_order_field = 'wikidata'
    
    def wikimedia_commons_link(self, obj):
        url = obj.wikimedia_commons_url()
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), obj.wikimedia_commons))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
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
        url = obj.wikipedia_url()
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), obj.wikipedia))
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'

@admin.register(WikidataEntry)
class WikidataEntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'wikidata_link', 'instance_of_link', 'sex_or_gender_link', 'occupations_link', 'grave_of_wikidata_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'burial_plot_reference', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'notes')
    search_fields = ('localizations__name', 'wikidata_id', 'instance_of', 'sex_or_gender', 'occupations', 'wikimedia_commons_category', 'wikimedia_commons_grave_category', 'grave_of_wikidata', 'burial_plot_reference', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_id', 'wikidata_link', 'instance_of', 'instance_of_link', 'sex_or_gender', 'sex_or_gender_link', 'occupations', 'occupations_link', 'grave_of_wikidata', 'grave_of_wikidata_link', 'wikimedia_commons_category', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category', 'wikimedia_commons_grave_category_link', 'burial_plot_reference', 'date_of_birth', 'date_of_birth_accuracy', 'date_of_death', 'date_of_death_accuracy']}),
    ]
    readonly_fields = ('name', 'wikidata_link', 'instance_of_link', 'sex_or_gender_link', 'occupations_link', 'grave_of_wikidata_link', 'wikimedia_commons_category_link', 'wikimedia_commons_grave_category_link', 'date_of_birth_with_accuracy', 'date_of_death_with_accuracy', 'created', 'modified')
    
    inlines = [
        WikidataLocalizedEntryInline,
    ]
    
    def name(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        language = Language.objects.filter(code=language_code).first()
        if language:
            wikidata_localized_entry = obj.localizations.filter(language=language).first()
            if wikidata_localized_entry:
                return wikidata_localized_entry.name
    name.short_description = _('name')
    
    def wikidata_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code, "wikidata_id")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_id'
    
    def instance_of_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code, "instance_of")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    instance_of_link.allow_tags = True
    instance_of_link.short_description = _('instance of')
    instance_of_link.admin_order_field = 'instance_of'
    
    def occupations_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code, "occupations")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    occupations_link.allow_tags = True
    occupations_link.short_description = _('occupations')
    occupations_link.admin_order_field = 'occupations'
    
    def sex_or_gender_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code, "sex_or_gender")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    sex_or_gender_link.allow_tags = True
    sex_or_gender_link.short_description = _('sex or gender')
    sex_or_gender_link.admin_order_field = 'sex_or_gender'
    
    def grave_of_wikidata_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_urls(language_code, "grave_of_wikidata")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    grave_of_wikidata_link.allow_tags = True
    grave_of_wikidata_link.short_description = _('grave_of:wikidata')
    grave_of_wikidata_link.admin_order_field = 'grave_of_wikidata'
    
    def wikimedia_commons_category_link(self, obj):
        url = obj.wikimedia_commons_category_url("wikimedia_commons_category")
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), obj.wikimedia_commons_category))
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def wikimedia_commons_grave_category_link(self, obj):
        url = obj.wikimedia_commons_category_url("wikimedia_commons_grave_category")
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), obj.wikimedia_commons_grave_category))
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
        wikidata_ids = [wikidata_entry.wikidata_id for wikidata_entry in queryset]
        sync_start = timezone.now()
        
        try:
            out = StringIO()
            call_command('sync_wikidata', wikidata_ids='|'.join(wikidata_ids), stdout=out)
            if out.getvalue():
                messages.error(request, _('An error occured. See the admin commands screen for more information.'))
            out.close()
        except:
            messages.error(request, sys.exc_info()[1])
            return
        
        # Redirect to pending modifications scren if needed
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        if pending_modifications:
            return HttpResponseRedirect(PendingModificationAdmin.modified_since_url(sync_start))
    sync_entry.short_description = _('Sync selected wikidata entries')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions=[delete_notes, sync_entry]

@admin.register(WikidataLocalizedEntry)
class WikidataLocalizedEntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_entry_link', 'language', 'name', 'wikidata_link', 'wikipedia_link', 'description', 'notes')
    list_filter = ('language',)
    search_fields = ('name', 'wikidata_entry__id', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_entry', 'language', 'name', 'wikipedia', 'description']}),
    ]
    readonly_fields = ('wikidata_entry_link', 'wikidata_link', 'wikipedia_link', 'created', 'modified')
    
    def wikidata_entry_link(self, obj):
        if obj.wikidata_entry:
            return mark_safe(u"<a href='%s'>%s</a>" % (change_page_url(obj.wikidata_entry), unicode(obj.wikidata_entry)))
    wikidata_entry_link.allow_tags = True
    wikidata_entry_link.short_description = _('wikidata entry')
    wikidata_entry_link.admin_order_field = 'wikidata_entry'
    
    def wikidata_link(self, obj):
        language_code = translation.get_language().split("-", 1)[0]
        wikidata_urls = obj.wikidata_entry.wikidata_urls(language_code, "wikidata_id")
        if wikidata_urls:
            result = [mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), wikidata)) for (wikidata, url) in wikidata_urls]
            return ';'.join(result)
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_entry'
    
    def wikipedia_link(self, obj):
        url = obj.wikipedia_url()
        if url:
            return mark_safe(u"<a href='%s'>%s</a>" % (url.replace("'","%27"), obj.wikipedia))
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def sync_entry(self, request, queryset):
        wikidata_ids = [wikidata_localized_entry.wikidata_entry.wikidata_id for wikidata_localized_entry in queryset]
        sync_start = timezone.now()
        
        try:
            out = StringIO()
            call_command('sync_wikidata', wikidata_ids='|'.join(wikidata_ids), stdout=out)
            if out.getvalue():
                messages.error(request, _('An error occured. See the admin commands screen for more information.'))
            out.close()
        except:
            messages.error(request, sys.exc_info()[1])
            return
        
        # Redirect to pending modifications scren if needed
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        if pending_modifications:
            return HttpResponseRedirect(PendingModificationAdmin.modified_since_url(sync_start))
    sync_entry.short_description = _('Sync selected localized wikidata entries')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_entry]

@admin.register(WikipediaPage)
class WikipediaPageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikidata_localized_entry_link', 'wikipedia_link', 'default_sort', 'intro_html', 'notes')
    list_filter = ('wikidata_localized_entry__language',)
    search_fields = ('wikidata_localized_entry__name', 'wikidata_localized_entry__wikipedia', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_localized_entry', 'wikipedia_link', 'default_sort', 'intro', 'intro_html']}),
    ]
    readonly_fields = ('wikidata_localized_entry_link', 'wikipedia_link', 'intro_html', 'created', 'modified')
    
    def wikidata_localized_entry_link(self, obj):
        if obj.wikidata_localized_entry:
            app_name = obj._meta.app_label
            reverse_name = obj.wikidata_localized_entry.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.wikidata_localized_entry.pk,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata_localized_entry)))
    wikidata_localized_entry_link.allow_tags = True
    wikidata_localized_entry_link.short_description = _('wikidata localized entry')
    wikidata_localized_entry_link.admin_order_field = 'wikidata_localized_entry'
    
    def wikipedia_link(self, obj):
        if obj.wikidata_localized_entry.wikipedia:
            url = u'https://{language}.wikipedia.org/wiki/{name}'.format(language=obj.wikidata_localized_entry.language.code, name=unicode(obj.wikidata_localized_entry.wikipedia)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata_localized_entry.wikipedia)))
    wikipedia_link.allow_tags = True
    wikipedia_link.short_description = _('wikipedia')
    wikipedia_link.admin_order_field = 'wikipedia'
    
    def intro_html(self, obj):
        return obj.intro
    intro_html.allow_tags = True
    intro_html.short_description = _('intro')
    intro_html.admin_order_field = 'intro'
    
    def sync_entry(self, request, queryset):
        wikidata_localized_entry_ids = queryset.values_list('wikidata_localized_entry_id', flat=True)
        wikidata_localized_entry_ids = [str(value) for value in wikidata_localized_entry_ids]
        sync_start = timezone.now()
        call_command('sync_wikipedia', wikidata_localized_entry_ids='|'.join(wikidata_localized_entry_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().pk,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_entry.short_description = _('Sync selected wikipedia pages')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_entry]

@admin.register(WikimediaCommonsCategory)
class WikimediaCommonsCategoryAdmin(admin.ModelAdmin):
    list_display = ('wikimedia_commons_id', 'wikimedia_commons_link', 'main_image_link', 'notes')
    search_fields = ('wikimedia_commons_id', 'main_image', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikimedia_commons_id', 'wikimedia_commons_link', 'main_image', 'main_image_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'main_image_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        url = u'https://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons_id)).replace("'","%27")
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_id)))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons category')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons_id'
    
    def main_image_link(self, obj):
        if obj.main_image:
            url = u'https://commons.wikimedia.org/wiki/{file}'.format(file=unicode(obj.main_image).replace("'","%27"))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.main_image)))
    main_image_link.allow_tags = True
    main_image_link.short_description = _('main image')
    main_image_link.admin_order_field = 'main_image'
    
    def sync_page(self, request, queryset):
        wikimedia_commons_categories = []
        for wikimedia_commons_category in queryset:
            wikimedia_commons_categories.append(wikimedia_commons_category.wikimedia_commons_id)
        sync_start = timezone.now()
        call_command('sync_wikimedia_commons_categories', wikimedia_commons_categories='|'.join(wikimedia_commons_categories))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().pk,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_page.short_description = _('Sync selected wikimedia commons categories')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_page]

@admin.register(WikimediaCommonsFile)
class WikimediaCommonsFileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'notes')
    search_fields = ('wikimedia_commons_id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikimedia_commons_id', 'wikimedia_commons_link', 'original_url', 'original_url_link', 'thumbnail_url', 'thumbnail_url_link']}),
    ]
    readonly_fields = ('wikimedia_commons_link', 'original_url_link', 'thumbnail_url_link', 'created', 'modified')
    
    def wikimedia_commons_link(self, obj):
        url = u'https://commons.wikimedia.org/wiki/{name}'.format(name=unicode(obj.wikimedia_commons_id)).replace("'","%27")
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_id)))
    wikimedia_commons_link.allow_tags = True
    wikimedia_commons_link.short_description = _('wikimedia commons file')
    wikimedia_commons_link.admin_order_field = 'wikimedia_commons_id'
    
    def original_url_link(self, obj):
        if obj.original_url:
            return mark_safe(u"<a href='%s'>%s</a>" % (obj.original_url, _('original image')))
    original_url_link.allow_tags = True
    original_url_link.short_description = _('original url')
    original_url_link.admin_order_field = 'original_url'
    
    def thumbnail_url_link(self, obj):
        if obj.thumbnail_url:
            result = u'<div style="background: url({url}); width:150px; height:150px; background-position:center; background-size:cover;"><a href="{url}"><img width=150 height=150/></a></div>'.format(url=obj.thumbnail_url)
            return mark_safe(result)
    thumbnail_url_link.allow_tags = True
    thumbnail_url_link.short_description = _('thumbnail url')
    thumbnail_url_link.admin_order_field = 'thumbnail_url'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

class SuperLachaiseWikidataRelationInline(admin.StackedInline):
    model = SuperLachaisePOI.wikidata_entries.through
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['wikidata_entry', 'name', 'relation_type']}),
    ]
    readonly_fields = ('name',)
    
    def name(self, obj):
        names = {}
        for wikidata_localized_entry in obj.wikidata_entry.localizations.all():
            if not wikidata_localized_entry.name in names:
                names[wikidata_localized_entry.name] = []
            names[wikidata_localized_entry.name].append(wikidata_localized_entry.language.code)
        
        if len(names) > 0:
            result = []
            for name, languages in names.iteritems():
                result.append('(%s)%s' % (','.join(languages), name))
            return '; '.join(result)
        
        return obj.wikidata_entry.wikidata_id
    name.short_description = _('name')
    
    verbose_name = "wikidata entry"
    verbose_name_plural = "wikidata entries"

class SuperLachaiseLocalizedPOIInline(admin.StackedInline):
    model = SuperLachaiseLocalizedPOI
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'name', 'sorting_name', 'description', 'created', 'modified']}),
    ]
    readonly_fields = ('created', 'modified')

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
    list_display = ('__unicode__', 'openstreetmap_element_link', 'wikidata_entries_link', 'wikimedia_commons_category_link', 'main_image_link', 'superlachaise_categories_link', 'modified', 'notes')
    list_filter = ('superlachaise_categories',)
    search_fields = ('openstreetmap_element__name', 'wikidata_entries__id', 'wikidata_entries__localizations__name', 'wikimedia_commons_category__id', 'main_image__id', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['openstreetmap_element', 'wikimedia_commons_category', 'main_image', 'superlachaise_categories_link']}),
    ]
    readonly_fields = ('openstreetmap_element_link', 'wikidata_entries_link', 'wikimedia_commons_category_link', 'main_image_link', 'superlachaise_categories_link', 'created', 'modified')
    filter_horizontal = ('superlachaise_categories',)
    
    inlines = [
        SuperLachaiseLocalizedPOIInline,
        SuperLachaiseWikidataRelationInline,
        SuperLachaiseCategoryRelationInline,
    ]
    
    def openstreetmap_element_link(self, obj):
        if obj.openstreetmap_element:
            app_name = obj._meta.app_label
            reverse_name = obj.openstreetmap_element.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.openstreetmap_element.pk,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.openstreetmap_element)))
    openstreetmap_element_link.allow_tags = True
    openstreetmap_element_link.short_description = _('openstreetmap element')
    openstreetmap_element_link.admin_order_field = 'openstreetmap_element'
    
    def wikidata_entries_link(self, obj):
        result = []
        for wikidata_entry_relation in obj.superlachaisewikidatarelation_set.all():
            app_name = obj._meta.app_label
            reverse_name = 'wikidataentry'
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(wikidata_entry_relation.wikidata_entry_id,))
            text = wikidata_entry_relation.relation_type + u':' + wikidata_entry_relation.wikidata_entry_id
            result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, text)))
        return ';'.join(result)
    wikidata_entries_link.allow_tags = True
    wikidata_entries_link.short_description = _('wikidata entries')
    wikidata_entries_link.admin_order_field = 'wikidata_entries'
    
    def wikimedia_commons_category_link(self, obj):
        if obj.wikimedia_commons_category:
            app_name = obj._meta.app_label
            reverse_name = obj.wikimedia_commons_category.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.wikimedia_commons_category.pk,)).replace("'","%27")
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikimedia_commons_category)))
    wikimedia_commons_category_link.allow_tags = True
    wikimedia_commons_category_link.short_description = _('wikimedia commons category')
    wikimedia_commons_category_link.admin_order_field = 'wikimedia_commons_category'
    
    def main_image_link(self, obj):
        if obj.main_image:
            app_name = obj._meta.app_label
            reverse_name = obj.main_image.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(obj.main_image.pk,)).replace("'","%27")
            result = u'<div style="background: url({image_url}); width:150px; height:150px; background-position:center; background-size:cover;"><a href="{url}"><img width=150 height=150/></a></div>'.format(image_url=obj.main_image.thumbnail_url, url=url)
            return mark_safe(result)
    main_image_link.allow_tags = True
    main_image_link.short_description = _('main image')
    main_image_link.admin_order_field = 'main_image'
    
    def superlachaise_categories_link(self, obj):
        result = []
        for superlachaise_category in obj.superlachaise_categories.all():
            app_name = obj._meta.app_label
            reverse_name = superlachaise_category.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(superlachaise_category.code,))
            result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(superlachaise_category))))
        return ';'.join(result)
    superlachaise_categories_link.allow_tags = True
    superlachaise_categories_link.short_description = _('superlachaise categories')
    superlachaise_categories_link.admin_order_field = 'superlachaise_categories'
    
    def sync_page(self, request, queryset):
        openstreetmap_element_ids = []
        for superlachaise_poi in queryset:
            openstreetmap_element_ids.append(superlachaise_poi.openstreetmap_element_id)
        sync_start = timezone.now()
        call_command('sync_superlachaise_pois', openstreetmap_element_ids='|'.join(openstreetmap_element_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().pk,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_page.short_description = _('Sync selected superlachaise POIs')
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes, sync_page]

@admin.register(SuperLachaiseLocalizedPOI)
class SuperLachaiseLocalizedPOIAdmin(admin.ModelAdmin):
    list_display = ('language', 'name', 'sorting_name', 'superlachaise_poi_link', 'description', 'modified', 'notes')
    list_filter = ('language',)
    search_fields = ('name', 'description', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['language', 'name', 'sorting_name', 'superlachaise_poi', 'description']}),
    ]
    readonly_fields = ('superlachaise_poi_link', 'created', 'modified')
    
    def superlachaise_poi_link(self, obj):
        app_name = obj._meta.app_label
        reverse_name = obj.superlachaise_poi.__class__.__name__.lower()
        reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
        url = reverse(reverse_path, args=(obj.superlachaise_poi.pk,))
        return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.superlachaise_poi)))
    superlachaise_poi_link.allow_tags = True
    superlachaise_poi_link.short_description = _('superlachaise poi')
    superlachaise_poi_link.admin_order_field = 'superlachaise_poi'
    
    def delete_notes(self, request, queryset):
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    def sync_page(self, request, queryset):
        openstreetmap_element_ids = []
        for superlachaise_localized_poi in queryset:
            openstreetmap_element_ids.append(superlachaise_localized_poi.superlachaise_poi.openstreetmap_element_id)
        sync_start = timezone.now()
        call_command('sync_superlachaise_pois', openstreetmap_element_ids='|'.join(openstreetmap_element_ids))
        pending_modifications = PendingModification.objects.filter(modified__gte=sync_start)
        
        if pending_modifications:
            # Open modification page with filter
            app_name = PendingModification._meta.app_label
            reverse_name = PendingModification.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            split_url = reverse(reverse_path, args=(pending_modifications.first().pk,)).split('/')
            split_url[len(split_url) - 2] = u'?modified__gte=%s' % (sync_start.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
            url = '/'.join(split_url[0:len(split_url) - 1])
            return HttpResponseRedirect(url)
    sync_page.short_description = _('Sync selected superlachaise localized POIs')
    
    actions = [delete_notes, sync_page]

class SuperLachaiseLocalizedCategoryInline(admin.StackedInline):
    model = SuperLachaiseLocalizedCategory
    extra = 0
    
    fieldsets = [
        (None, {'fields': ['language', 'name']}),
    ]

@admin.register(SuperLachaiseCategory)
class SuperLachaiseCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'values', 'members_count', 'wikidata_occupations_count', 'notes')
    list_filter = ('type',)
    search_fields = ('code', 'type', 'values', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['code', 'type', 'values']}),
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
        queryset.update(notes=u'')
    delete_notes.short_description = _('Delete notes')
    
    actions = [delete_notes]

@admin.register(WikidataOccupation)
class WikidataOccupationAdmin(admin.ModelAdmin):
    list_display = ('wikidata_id', 'name', 'wikidata_link', 'superlachaise_category', 'used_in_link', 'notes')
    list_filter = ('superlachaise_category',)
    list_editable = ('superlachaise_category',)
    search_fields = ('wikidata_id', 'name', 'used_in__id', 'used_in__localizations__name', 'notes',)
    
    fieldsets = [
        (None, {'fields': ['created', 'modified', 'notes']}),
        (None, {'fields': ['wikidata_id', 'name', 'wikidata_link', 'superlachaise_category', 'used_in']}),
    ]
    filter_horizontal = ('used_in',)
    readonly_fields = ('wikidata_link', 'used_in_link', 'created', 'modified')
    
    def wikidata_link(self, obj):
        if obj.wikidata_id:
            language = translation.get_language().split("-", 1)[0]
            url = u'https://www.wikidata.org/wiki/{name}?userlang={language}&uselang={language}'.format(name=unicode(obj.wikidata_id), language=language)
            return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.wikidata_id)))
    wikidata_link.allow_tags = True
    wikidata_link.short_description = _('wikidata')
    wikidata_link.admin_order_field = 'wikidata_id'
    
    def used_in_count(self, obj):
        return obj.used_in.count()
    used_in_count.short_description = _('used in count')
    
    def used_in_link(self, obj):
        result = []
        for wikidata_entry in obj.used_in.all():
            app_name = obj._meta.app_label
            reverse_name = wikidata_entry.__class__.__name__.lower()
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            url = reverse(reverse_path, args=(wikidata_entry.pk,))
            result.append(mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(wikidata_entry))))
        return ';'.join(result)
    used_in_link.allow_tags = True
    used_in_link.short_description = _('used in')
    used_in_link.admin_order_field = 'used_in'
    
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
    
    @classmethod
    def modified_since_url(cls, modified_since):
        """ Return an URL for the pending modifications admin page where the entries are filtered by modified date greater than the specified date """
        app_name = PendingModification._meta.app_label
        reverse_name = PendingModification.__name__.lower()
        reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
        split_url = reverse(reverse_path, args=(1,)).split('/')
        split_url[len(split_url) - 2] = u'?modified__gte=%s' % (modified_since.strftime('%Y-%m-%d+%H:%M:%S') + '%2B00%3A00')
        url = '/'.join(split_url[0:len(split_url) - 1])
        return url
    
    def target_object_link(self, obj):
        try:
            if obj.target_object():
                app_name = obj._meta.app_label
                reverse_name = obj.target_object_class.lower()
                reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
                url = reverse(reverse_path, args=(obj.target_object().pk,)).replace("'","%27")
                return mark_safe(u"<a href='%s'>%s</a>" % (url, unicode(obj.target_object())))
        except:
            pass
    target_object_link.allow_tags = True
    target_object_link.short_description = _('target object')
    
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
