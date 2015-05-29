# -*- coding: utf-8 -*-

"""
sync_OpenStreetMap.py
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

import datetime, json, sys, time, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def none_to_blank(s):
    if s is None:
        return u''
    return unicode(s)

class Command(BaseCommand):
    
    def request_wikidata_with_ids(self, wikidata_codes):
        # List languages to request
        languages = []
        for language in Language.objects.all():
            languages.append(language.code)
        
        # List props to request
        props = ['labels', 'descriptions', 'claims', 'sitelinks']
        
        max_items_per_request = 25
        
        result = {}
        i = 0
        while i < len(wikidata_codes):
            wikidata_codes_page = wikidata_codes[i : min(len(wikidata_codes), i + max_items_per_request)]
            
            # Request properties
            url = "http://www.wikidata.org/w/api.php?languages={languages}&action=wbgetentities&ids={ids}&props={props}&format=json"\
                .format(languages='|'.join(languages), ids='|'.join(wikidata_codes_page), props='|'.join(props))
            request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
            u = urllib2.urlopen(request)
            
            # Parse result
            data = u.read()
            json_result = json.loads(data)
            
            # Add entities to result
            result.update(json_result['entities'])
            
            i = i + max_items_per_request
        
        return result
    
    def request_wikidata_with_titles(self, wikidata_titles):
        # List languages to request
        languages = []
        for language in Language.objects.all():
            languages.append(language.code)
        
        # List props to request
        props = ['labels', 'descriptions', 'claims', 'sitelinks']
        
        max_items_per_request = 25
        
        result = {}
        
        for language_code, titles in wikidata_titles.iteritems():
            i = 0
            while i < len(titles):
                titles_page = titles[i : min(len(titles), i + max_items_per_request)]
            
                # Request properties
                url = u"http://www.wikidata.org/w/api.php?languages={languages}&action=wbgetentities&sites={sites}&titles={titles}&props={props}&format=json"\
                    .format(languages='|'.join(languages), titles=urllib2.quote('|'.join(titles_page).encode('utf8'), '|'), props='|'.join(props), sites=language_code + 'wiki')
                request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
                u = urllib2.urlopen(request)
                
                # Parse result
                data = u.read()
                json_result = json.loads(data)
            
                # Add entities to result
                result.update(json_result['entities'])
            
                i = i + max_items_per_request
        
        return result
    
    def get_instance_of(self, entity):
        try:
            p31 = entity['claims']['P31']
            
            return 'Q' + str(p31[0]['mainsnak']['datavalue']['value']['numeric-id'])
        except:
            return u''
    
    def get_wikimedia_commons_category(self, entity):
        try:
            # Use P373
            p373 = entity['claims']['P373']
            
            wikimedia_commons = p373[0]['mainsnak']['datavalue']['value']
            
            # Delete random trailing character
            return wikimedia_commons.replace(u'\u200e',u'')
        except:
            return none_to_blank(None)
    
    def get_wikimedia_commons_grave_category(self, entity):
        try:
            p119 = entity['claims']['P119']
            p373 = p119[0]['qualifiers']['P373']
            
            wikimedia_commons = p373[0]['datavalue']['value']
            
            # Delete random trailing character
            return wikimedia_commons.replace(u'\u200e',u'')
        except:
            return none_to_blank(None)
    
    def get_date(self, entity, date_code):
        try:
            date = entity['claims'][date_code]
            
            date_value = date[0]['mainsnak']['datavalue']['value']
            
            precision_string = date_value['precision']
            date_string = date_value['time']
            
            date = datetime.date(*time.strptime(date_string[1:11], "%Y-%m-%d")[:3])
            
            # Convert accuracy
            if precision_string == 9:
                accuracy = WikidataEntry.YEAR
            elif precision_string == 10:
                accuracy = WikidataEntry.MONTH
            elif precision_string == 11:
                accuracy = WikidataEntry.DAY
            else:
                raise BaseException
            
            return (date, accuracy)
        except:
            return (None, none_to_blank(None))
    
    def get_name(self, entity, language_code):
        try:
            name = entity['labels'][language_code]
            
            return name['value']
        except:
            return none_to_blank(None)
    
    def get_wikipedia(self, entity, language_code):
        try:
            wikipedia = entity['sitelinks'][language_code + 'wiki']
            
            return wikipedia['title']
        except:
            return none_to_blank(None)
    
    def get_description(self, entity, language_code):
        try:
            description = entity['descriptions'][language_code]
            
            return description['value']
        except:
            return none_to_blank(None)
    
    def get_values_from_entity(self, entity):
        result = {}
        
        instance_of = self.get_instance_of(entity)
        if instance_of == 'Q5':
            result['instance_of'] = instance_of
            result['wikimedia_commons_category'] = self.get_wikimedia_commons_category(entity)
            result['wikimedia_commons_grave_category'] = self.get_wikimedia_commons_grave_category(entity)
            result['date_of_birth'], result['date_of_birth_accuracy'] = self.get_date(entity, 'P569')
            result['date_of_death'], result['date_of_death_accuracy'] = self.get_date(entity, 'P570')
        else:
            result['instance_of'] = instance_of
            result['wikimedia_commons_category'] = self.get_wikimedia_commons_category(entity)
            result['wikimedia_commons_grave_category'] = none_to_blank(None)
            result['date_of_birth'], result['date_of_birth_accuracy'] = (None, none_to_blank(None))
            result['date_of_death'], result['date_of_death_accuracy'] = (None, none_to_blank(None))
        
        current_language = translation.get_language().split("-", 1)[0]
        result['name'] = u''
        for language in Language.objects.all():
            name = self.get_name(entity, language.code)
            if name:
                result['name'] = name
            if language.code == current_language:
                break
        
        return result
    
    def get_localized_values_from_entity(self, entity, language_code):
        result = {
            language_code + ':name': self.get_name(entity, language_code),
            language_code + ':wikipedia': self.get_wikipedia(entity, language_code),
            language_code + ':description': self.get_description(entity, language_code),
        }
        
        for key, value in result.iteritems():
            if value != u'' and not value is None:
                return result
        
        return None
    
    def sync_wikidata(self, wikidata_ids):
        wikidata_codes = []
        wikipedia_titles = {}
        
        # List wikidata codes and/or wikipedia titles in openstreetmap objects
        if wikidata_ids:
            wikidata_codes = wikidata_ids.split('|')
        else:
            for openstreetmap_element in OpenStreetMapElement.objects.all():
                if self.sync_from_wikidata and openstreetmap_element.wikidata:
                    for link in openstreetmap_element.wikidata.split(';'):
                        if not link in wikidata_codes:
                            wikidata_codes.append(link)
                if self.sync_from_wikipedia and openstreetmap_element.wikipedia:
                    language_code = openstreetmap_element.wikipedia.split(':')[0]
                    if not language_code in wikipedia_titles:
                        wikipedia_titles[language_code] = []
                    for link in openstreetmap_element.wikipedia.split(':')[1].split(';'):
                        if not link in wikipedia_titles[language_code]:
                            wikipedia_titles[language_code].append(link)
                if self.sync_from_wikipedia and openstreetmap_element.subject_wikipedia:
                    language_code = openstreetmap_element.subject_wikipedia.split(':')[0]
                    if not language_code in wikipedia_titles:
                        wikipedia_titles[language_code] = []
                    for link in openstreetmap_element.subject_wikipedia.split(':')[1].split(';'):
                        if not link in wikipedia_titles[language_code]:
                            wikipedia_titles[language_code].append(link)
        
        # Request wikidata entities
        entities = {}
        if wikidata_codes:
            entities.update(self.request_wikidata_with_ids(wikidata_codes))
        if wikipedia_titles:
            entities.update(self.request_wikidata_with_titles(wikipedia_titles))
        
        for code, entity in entities.iteritems():
            if '-' in code:
                # Wikipedia entry not found
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=entity['site'] + ': ' + entity['title'])
                pendingModification.action = PendingModification.ERROR
                pendingModification.modified_fields = json.dumps(entity, default=date_handler)
                
                pendingModification.full_clean()
                pendingModification.save()
                self.error_objects = self.error_objects + 1
                
                continue
            
            # Get element in database if it exists
            wikidata_entry = WikidataEntry.objects.filter(id=code).first()
            
            if not wikidata_entry:
                # Creation
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=code)
                
                values_dict = self.get_values_from_entity(entity)
                for language in Language.objects.all():
                    localized_values_dict = self.get_localized_values_from_entity(entity, language.code)
                    if localized_values_dict:
                        values_dict.update(localized_values_dict)
                
                pendingModification.action = PendingModification.CREATE
                pendingModification.modified_fields = json.dumps(values_dict, default=date_handler)
                
                pendingModification.full_clean()
                pendingModification.save()
                self.created_objects = self.created_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Search for modifications
                modified_values = {}
                
                values_dict = self.get_values_from_entity(entity)
                for field, value in values_dict.iteritems():
                    if value != getattr(wikidata_entry, field):
                        modified_values[field] = value
                
                for language in Language.objects.all():
                    values_dict = self.get_localized_values_from_entity(entity, language.code)
                    localized_wikidata_entry = LocalizedWikidataEntry.objects.filter(parent=wikidata_entry, language=language).first()
                    
                    if values_dict:
                        if not localized_wikidata_entry:
                            modified_values.update(values_dict)
                        else:
                            for field, value in values_dict.iteritems():
                                if value != getattr(localized_wikidata_entry, field.split(':')[1]):
                                    modified_values[field] = value
                    else:
                        if localized_wikidata_entry:
                            modified_values[language.code + u':'] = None
                
                if modified_values:
                    # Get or create a modification
                    pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=code)
                    pendingModification.modified_fields = json.dumps(modified_values, default=date_handler)
                    pendingModification.action = PendingModification.MODIFY
                
                    pendingModification.full_clean()
                    pendingModification.save()
                    self.modified_objects = self.modified_objects + 1
                
                    if self.auto_apply:
                        pendingModification.apply_modification()
                else:
                    # Delete the previous modification if any
                    pendingModification = PendingModification.objects.filter(target_object_class="WikidataEntry", target_object_id=code).first()
                    if pendingModification:
                        pendingModification.delete()
        
        if not wikidata_ids:
            # Delete pending creations if element was deleted in Wikidata
            for pendingModification in PendingModification.objects.filter(target_object_class="WikidataEntry", action=PendingModification.CREATE):
                if not pendingModification.target_object_id in entities:
                    pendingModification.delete()
        
            # Look for deleted elements
            for wikidata_entry in WikidataEntry.objects.all():
                if not wikidata_entry.id in entities:
                    pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=wikidata_entry.id)
                
                    pendingModification.action = PendingModification.DELETE
                    pendingModification.modified_fields = u''
                
                    pendingModification.full_clean()
                    pendingModification.save()
                    self.deleted_objects = self.deleted_objects + 1
                
                    if self.auto_apply:
                        pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--wikidata_ids',
            action='store',
            dest='wikidata_ids')
    
    def handle(self, *args, **options):
        
        translation.activate(settings.LANGUAGE_CODE)
        
        self.auto_apply = (Setting.objects.get(category='Wikidata', key=u'auto_apply_modifications').value == 'true')
        self.sync_from_wikidata = (Setting.objects.get(category='Wikidata', key=u'sync_from_wikidata').value == 'true')
        self.sync_from_wikipedia = (Setting.objects.get(category='Wikidata', key=u'sync_from_wikipedia').value == 'true')
        
        admin_command = AdminCommand.objects.get(name='sync_wikidata')
        
        try:
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.error_objects = 0
            
            PendingModification.objects.filter(target_object_class="WikidataEntry", action=PendingModification.ERROR).delete()
            
            self.sync_wikidata(options['wikidata_ids'])
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.deleted_objects > 0:
                result_list.append(_('{nb} object(s) deleted').format(nb=self.deleted_objects))
            if self.error_objects > 0:
                result_list.append(_('{nb} error(s)').format(nb=self.error_objects))
            
            if result_list:
                admin_command.last_result = ', '.join(result_list)
            else:
                admin_command.last_result = _("No modifications")
        except:
            exception = sys.exc_info()[0]
            admin_command.last_result = exception.__class__.__name__ + ': ' + traceback.format_exc()
        
        admin_command.last_executed = timezone.now()
        admin_command.save()
        
        translation.deactivate()
