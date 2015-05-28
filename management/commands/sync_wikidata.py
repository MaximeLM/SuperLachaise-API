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
    
    def request_wikidata(self, wikidata_codes):
        # List languages to request
        languages = []
        for language in Language.objects.all():
            languages.append(language.code)
        
        # List props to request
        props = ['labels', 'descriptions', 'claims', 'sitelinks']
        
        result = {}
        i = 0
        while i < len(wikidata_codes):
            wikidata_codes_page = wikidata_codes[i : max(len(wikidata_codes) - 1, i + 49)]
            
            # Request properties
            url = "http://www.wikidata.org/w/api.php?languages={languages}&action=wbgetentities&ids={ids}&props={props}&format=json"\
                .format(languages='|'.join(languages), ids='|'.join(wikidata_codes_page), props='|'.join(props))
            request = urllib2.Request(url, headers={"User-Agent" : "fill_from_wiki.py extraction tool lm.maxime@gmail.com"})
            u = urllib2.urlopen(request)
            
            # Parse result
            data = u.read()
            json_result = json.loads(data)
        
            # Add entities to result
            result.update(json_result['entities'])
            
            i = i + 50
        
        return result
    
    def get_is_human(self, entity):
        try:
            p31 = entity['claims']['P31']
            
            instance_of = p31[0]['mainsnak']['datavalue']['value']['numeric-id']
            
            return (instance_of == 5)
        except:
            #traceback.print_exc()
            return False
    
    def get_wikimedia_commons(self, qualifiers):
        try:
            p373 = qualifiers['P373']
            
            wikimedia_commons = p373[0]['datavalue']['value']
            
            # Delete random trailing character
            return wikimedia_commons.replace(u'\u200e',u'')
        except:
            return none_to_blank(None)
    
    def get_place_wikimedia_commons(self, entity):
        try:
            return self.get_wikimedia_commons(entity['claims'])
        except:
            return none_to_blank(None)
    
    def get_person_wikimedia_commons(self, entity):
        try:
            p119 = entity['claims']['P119']
            
            return self.get_wikimedia_commons(p119[0]['qualifiers'])
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
                raise
            
            return (date, accuracy)
        except:
            return (None, none_to_blank(None))
    
    def get_values_from_entity(self, entity):
        result = {}
        
        if self.get_is_human(entity):
            result['type'] = WikidataEntry.PERSON
            result['wikimedia_commons'] = self.get_person_wikimedia_commons(entity)
            result['date_of_birth'], result['date_of_birth_accuracy'] = self.get_date(entity, 'P569')
            result['date_of_death'], result['date_of_death_accuracy'] = self.get_date(entity, 'P570')
        else:
            result['type'] = WikidataEntry.PLACE
            result['wikimedia_commons'] = self.get_place_wikimedia_commons(entity)
            result['date_of_birth'], result['date_of_birth_accuracy'] = (None, none_to_blank(None))
            result['date_of_death'], result['date_of_death_accuracy'] = (None, none_to_blank(None))
        
        return result
    
    def sync_wikidata(self):
        # List wikidata codes in openstreetmap objects
        wikidata_codes = []
        for openstreetmap_element in OpenStreetMapElement.objects.all():
            if openstreetmap_element.wikidata and not openstreetmap_element.wikidata in wikidata_codes:
                wikidata_codes.append(openstreetmap_element.wikidata.replace(';','|'))
        
        # Request wikidata entities
        entities = self.request_wikidata(wikidata_codes)
        for code, entity in entities.iteritems():
            # Get element in database if it exists
            wikidata_entry = WikidataEntry.objects.filter(id=code).first()
            
            if not wikidata_entry:
                # Creation
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=code)
                
                values_dict = self.get_values_from_entity(entity)
                
                pendingModification.action = PendingModification.CREATE
                pendingModification.modified_fields = json.dumps(values_dict, default=date_handler)
                
                pendingModification.full_clean()
                pendingModification.save()
                self.created_objects = self.created_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Search for modifications
                values_dict = self.get_values_from_entity(entity)
                modified_values = {}
                
                for field, value in values_dict.iteritems():
                    if value != getattr(wikidata_entry, field):
                        modified_values[field] = value
                
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
    
    def handle(self, *args, **options):
        
        translation.activate(settings.LANGUAGE_CODE)
        
        self.auto_apply = (Setting.objects.get(category='Modifications', key=u'auto_apply').value == 'true')
        
        admin_command = AdminCommand.objects.get(name='sync_wikidata')
        
        try:
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_wikidata()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.deleted_objects > 0:
                result_list.append(_('{nb} object(s) deleted').format(nb=self.deleted_objects))
            
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
