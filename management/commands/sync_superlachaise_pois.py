# -*- coding: utf-8 -*-

"""
sync_wikidata.py
superlachaise_api

Created by Maxime Le Moine on 28/05/2015.
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

import datetime, json, os, sys, time, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def get_wikidata_entries(self, openstreetmap_element):
        result = []
        
        if openstreetmap_element.wikidata_combined:
            for wikidata in openstreetmap_element.wikidata_combined.split(';'):
                wikidata_id = wikidata.split(':')[-1]
                wikidata_entry = WikidataEntry.objects.filter(id=wikidata_id).first()
                if wikidata_entry:
                    if len(wikidata.split(':')) == 2:
                        relation_type = wikidata.split(':')[0]
                    elif wikidata_entry.instance_of == 'Q5':
                        relation_type = SuperLachaiseWikidataRelation.PERSON
                    else:
                        relation_type = SuperLachaiseWikidataRelation.NONE
                    result.append(relation_type + u':' + str(wikidata_entry.id))
                    
                    if wikidata_entry.grave_of_wikidata:
                        for grave_of_wikidata in wikidata_entry.grave_of_wikidata.split(';'):
                            grave_of_wikidata_entry = WikidataEntry.objects.filter(id=grave_of_wikidata).first()
                            if grave_of_wikidata_entry:
                                relation_type = SuperLachaiseWikidataRelation.PERSON
                                result.append(relation_type + u':' + str(grave_of_wikidata_entry.id))
        
        result.sort()
        return result
    
    def get_wikimedia_commons_category(self, openstreetmap_element, wikidata_fetched_entries):
        wikimedia_commons_categories = []
        if openstreetmap_element.wikimedia_commons:
            wikimedia_commons = openstreetmap_element.wikimedia_commons.split('Category:')[-1]
            if not wikimedia_commons in wikimedia_commons_categories:
                wikimedia_commons_categories.append(wikimedia_commons)
        for wikidata_fetched_entry in wikidata_fetched_entries:
            wikidata_entry = WikidataEntry.objects.get(id=wikidata_fetched_entry.split(':')[-1])
            if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                # Person relation
                wikimedia_commons = wikidata_entry.wikimedia_commons_grave_category
                if wikimedia_commons:
                    if not wikimedia_commons in wikimedia_commons_categories:
                        wikimedia_commons_categories.append(wikimedia_commons)
        
        if len(wikimedia_commons_categories) == 1:
            wikimedia_commons_category = WikimediaCommonsCategory.objects.filter(id=wikimedia_commons_categories[0]).first()
            if wikimedia_commons_category:
                return wikimedia_commons_category
            else:
                return None
        else:
            return None
    
    def get_main_image(self, wikimedia_commons_category):
        if wikimedia_commons_category and wikimedia_commons_category.main_image:
            result =  WikimediaCommonsFile.objects.filter(id=wikimedia_commons_category.main_image).first()
            if not result:
                print wikimedia_commons_category.main_image
            return result
        else:
            return None
    
    def get_superlachaise_poi_wikidata_entries(self, superlachaise_poi):
        result = []
        for wikidata_relation in superlachaise_poi.superlachaisewikidatarelation_set.all():
            result.append(wikidata_relation.relation_type + u':' + str(wikidata_relation.wikidata_entry_id))
        
        result.sort()
        return result
    
    def get_categories(self, openstreetmap_element, wikidata_fetched_entries):
        properties = {}
        
        if openstreetmap_element.nature:
            properties[SuperLachaiseCategory.ELEMENT_NATURE] = [openstreetmap_element.nature]
        
        sex_or_gender = []
        for wikidata_fetched_entry in wikidata_fetched_entries:
            wikidata_entry = WikidataEntry.objects.get(id=wikidata_fetched_entry.split(':')[-1])
            if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                # Person relation
                if wikidata_entry.sex_or_gender and not wikidata_entry.sex_or_gender in sex_or_gender:
                    sex_or_gender.append(wikidata_entry.sex_or_gender)
        properties[SuperLachaiseCategory.SEX_OR_GENDER] = sex_or_gender
        
        result = []
        for key, values in properties.iteritems():
            for value in values:
                for category in SuperLachaiseCategory.objects.filter(key=key):
                    if value in category.values.split(';') and not category.name in result:
                        result.append(category.name)
        
        result.sort()
        return result
    
    def get_superlachaise_poi_categories(self, superlachaise_poi):
        result = []
        for category in superlachaise_poi.categories.all():
            if not category.name in result:
                result.append(category.name)
        
        result.sort()
        return result
    
    def get_values_for_openstreetmap_element(self, openstreetmap_element):
        wikidata_entries = self.get_wikidata_entries(openstreetmap_element)
        wikimedia_commons_category = self.get_wikimedia_commons_category(openstreetmap_element, wikidata_entries)
        main_image = self.get_main_image(wikimedia_commons_category)
        categories = self.get_categories(openstreetmap_element, wikidata_entries)
        
        result = {
            'wikidata_entries': wikidata_entries,
            'wikimedia_commons_category_id': wikimedia_commons_category.id if wikimedia_commons_category else None,
            'main_image_id': main_image.id if main_image else None,
            'categories': categories,
        }
        
        return result
    
    def get_localized_values_for_openstreetmap_element(self, openstreetmap_element, language):
        return {}
    
    def sync_superlachaise_poi(self, openstreetmap_element_id):
        openstreetmap_element = OpenStreetMapElement.objects.get(id=openstreetmap_element_id)
        
        # Get element in database if it exists
        superlachaise_poi = SuperLachaisePOI.objects.filter(openstreetmap_element=openstreetmap_element).first()
        
        if not superlachaise_poi:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=openstreetmap_element_id)
            
            values_dict = self.get_values_for_openstreetmap_element(openstreetmap_element)
            for language in Language.objects.all():
                localized_values_dict = self.get_localized_values_for_openstreetmap_element(openstreetmap_element, language)
                if localized_values_dict:
                    values_dict.update(localized_values_dict)
            
            pendingModification.action = PendingModification.CREATE
            pendingModification.modified_fields = json.dumps(values_dict)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            # Search for modifications
            modified_values = {}
            
            values_dict = self.get_values_for_openstreetmap_element(openstreetmap_element)
            for field, value in values_dict.iteritems():
                if field == 'wikidata_entries':
                    superlachaise_poi_wikidata_entries = self.get_superlachaise_poi_wikidata_entries(superlachaise_poi)
                    if value != superlachaise_poi_wikidata_entries:
                        modified_values[field] = value
                elif field == 'categories':
                    superlachaise_poi_categories = self.get_superlachaise_poi_categories(superlachaise_poi)
                    if value != superlachaise_poi_categories:
                        modified_values[field] = value
                else:
                    if value != getattr(superlachaise_poi, field):
                        modified_values[field] = value
            
            for language in Language.objects.all():
                values_dict = self.get_localized_values_for_openstreetmap_element(openstreetmap_element, language)
                superlachaise_localized_poi = superlachaise_poi.localizations.filter(language=language).first()
                
                if values_dict:
                    if not superlachaise_localized_poi:
                        modified_values.update(values_dict)
                    else:
                        for field, value in values_dict.iteritems():
                            if value != getattr(superlachaise_localized_poi, field.split(':')[1]):
                                modified_values[field] = value
                else:
                    if superlachaise_localized_poi:
                        modified_values[language.code + u':'] = None
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=openstreetmap_element_id)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = PendingModification.MODIFY
            
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="SuperLachaisePOI", target_object_id=openstreetmap_element_id).first()
                if pendingModification:
                    pendingModification.delete()
    
    def sync_superlachaise_pois(self, param_openstreetmap_element_ids):
        # Get OpenStreetMap elements
        if param_openstreetmap_element_ids:
            openstreetmap_element_ids = param_openstreetmap_element_ids.split('|')
        else:
            openstreetmap_element_ids = []
            for openstreetmap_element in OpenStreetMapElement.objects.all():
                openstreetmap_element_ids.append(openstreetmap_element.id)
        
        for openstreetmap_element_id in openstreetmap_element_ids:
            self.sync_superlachaise_poi(openstreetmap_element_id)
        
        if not param_openstreetmap_element_ids:
            # Delete pending creations if element was not fetched
            for pendingModification in PendingModification.objects.filter(target_object_class="SuperLachaisePOI", action=PendingModification.CREATE):
                if not pendingModification.target_object_id in openstreetmap_element_ids:
                    pendingModification.delete()
        
            # Look for deleted elements
            for superlachaise_poi in SuperLachaisePOI.objects.all():
                if not superlachaise_poi.openstreetmap_element.id in openstreetmap_element_ids:
                    pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=uperlachaise_poi.openstreetmap_element.id)
                
                    pendingModification.action = PendingModification.DELETE
                    pendingModification.modified_fields = u''
                
                    pendingModification.full_clean()
                    pendingModification.save()
                    self.deleted_objects = self.deleted_objects + 1
                
                    if self.auto_apply:
                        pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--openstreetmap_element_ids',
            action='store',
            dest='openstreetmap_element_ids')
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(category='SuperLachaise POI', key=u'auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_superlachaise_pois(options['openstreetmap_element_ids'])
            
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
