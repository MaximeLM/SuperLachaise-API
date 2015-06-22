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
from django.db.models import Q
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def print_unicode(str):
    print str.encode('utf-8')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class Command(BaseCommand):
    
    def get_wikidata_entries(self, openstreetmap_element):
        result = []
        
        if openstreetmap_element.wikidata:
            for wikidata in openstreetmap_element.wikidata.split(';'):
                wikidata_id = wikidata.split(':')[-1]
                wikidata_entry = WikidataEntry.objects.filter(wikidata_id=wikidata_id, deleted=False).first()
                if wikidata_entry:
                    if len(wikidata.split(':')) == 2:
                        relation_type = wikidata.split(':')[0]
                    elif 'Q5' in wikidata_entry.instance_of.split(';'):
                        relation_type = SuperLachaiseWikidataRelation.PERSON
                    else:
                        relation_type = SuperLachaiseWikidataRelation.NO_TYPE
                    result.append(relation_type + u':' + str(wikidata_entry.wikidata_id))
                    
                    if wikidata_entry.grave_of_wikidata:
                        for grave_of_wikidata in wikidata_entry.grave_of_wikidata.split(';'):
                            grave_of_wikidata_entry = WikidataEntry.objects.filter(wikidata_id=grave_of_wikidata).first()
                            if grave_of_wikidata_entry:
                                relation_type = SuperLachaiseWikidataRelation.PERSON
                                result.append(relation_type + u':' + str(grave_of_wikidata_entry.wikidata_id))
        
        result.sort()
        return result
    
    def get_wikimedia_commons_category(self, openstreetmap_element, wikidata_fetched_entries):
        wikimedia_commons_categories = []
        if openstreetmap_element.wikimedia_commons:
            wikimedia_commons = openstreetmap_element.wikimedia_commons
            if not wikimedia_commons in wikimedia_commons_categories:
                wikimedia_commons_categories.append(wikimedia_commons)
        for wikidata_fetched_entry in wikidata_fetched_entries:
            wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
            if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON and wikidata_entry.wikimedia_commons_grave_category:
                # Person relation
                wikimedia_commons = 'Category:' + wikidata_entry.wikimedia_commons_grave_category
                if not wikimedia_commons in wikimedia_commons_categories:
                    wikimedia_commons_categories.append(wikimedia_commons)
            if wikidata_entry.wikimedia_commons_category:
                sync_category = False
                for instance_of in wikidata_entry.instance_of.split(';'):
                    if instance_of in self.synced_instance_of:
                        sync_category = True
                        break
                if sync_category:
                    wikimedia_commons = 'Category:' + wikidata_entry.wikimedia_commons_category
                    if not wikimedia_commons in wikimedia_commons_categories:
                        wikimedia_commons_categories.append(wikimedia_commons)
        
        if len(wikimedia_commons_categories) == 1:
            return WikimediaCommonsCategory.objects.filter(wikimedia_commons_id=wikimedia_commons_categories[0], deleted=False).first()
        else:
            return None
    
    def get_main_image(self, wikimedia_commons_category):
        if wikimedia_commons_category and wikimedia_commons_category.main_image:
            result =  WikimediaCommonsFile.objects.filter(wikimedia_commons_id=wikimedia_commons_category.main_image).first()
            return result
        else:
            return None
    
    def get_superlachaise_categories(self, openstreetmap_element, wikidata_fetched_entries):
        properties = {}
        
        if openstreetmap_element.nature:
            properties[SuperLachaiseCategory.ELEMENT_NATURE] = [openstreetmap_element.nature]
            if openstreetmap_element.nature == u'tomb':
                if not SuperLachaiseCategory.OCCUPATION in properties:
                    properties[SuperLachaiseCategory.OCCUPATION] = []
        
        for wikidata_fetched_entry in wikidata_fetched_entries:
            wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
            if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                # Person relation
                if not SuperLachaiseCategory.OCCUPATION in properties:
                    properties[SuperLachaiseCategory.OCCUPATION] = []
                
                if wikidata_entry.sex_or_gender:
                    if not SuperLachaiseCategory.SEX_OR_GENDER in properties:
                        properties[SuperLachaiseCategory.SEX_OR_GENDER] = []
                    if not wikidata_entry.sex_or_gender in properties[SuperLachaiseCategory.SEX_OR_GENDER]:
                        properties[SuperLachaiseCategory.SEX_OR_GENDER].append(wikidata_entry.sex_or_gender)
                
                if wikidata_entry.occupations:
                    for occupation in wikidata_entry.occupations.split(';'):
                        if not occupation in properties[SuperLachaiseCategory.OCCUPATION]:
                            properties[SuperLachaiseCategory.OCCUPATION].append(occupation)
        
        result = []
        for type, values in properties.iteritems():
            superlachaise_categories = []
            for value in values:
                for superlachaise_category in SuperLachaiseCategory.objects.filter(type=type, deleted=False).exclude(code__in=superlachaise_categories, values__exact=''):
                    if value in superlachaise_category.values.split(';'):
                        superlachaise_categories.append(superlachaise_category.code)
                superlachaise_categories.extend(SuperLachaiseCategory.objects.filter(type=type, deleted=False, wikidata_occupations__wikidata_id=value).exclude(code__in=superlachaise_categories).values_list('code', flat=True))
            if not superlachaise_categories and type == SuperLachaiseCategory.OCCUPATION:
                superlachaise_categories = [u'other']
            result.extend(superlachaise_categories)
        
        result.sort()
        return result
    
    def get_dates(self, wikidata_fetched_entries):
        unique_wikidata_entry = None
        for wikidata_fetched_entry in wikidata_fetched_entries:
            if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                if not unique_wikidata_entry:
                    unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                else:
                    unique_wikidata_entry = None
                    break
        
        result = {}
        if unique_wikidata_entry:
            result = {
                "date_of_birth": unique_wikidata_entry.date_of_birth,
                "date_of_death": unique_wikidata_entry.date_of_death,
                "date_of_birth_accuracy": unique_wikidata_entry.date_of_birth_accuracy,
                "date_of_death_accuracy": unique_wikidata_entry.date_of_death_accuracy,
            }
        
        return result
    
    def get_burial_plot_reference(self, wikidata_fetched_entries):
        result = u''
        
        for wikidata_fetched_entry in wikidata_fetched_entries:
            wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
            
            if wikidata_entry.burial_plot_reference:
                if not result:
                    result = wikidata_entry.burial_plot_reference
                elif not result == wikidata_entry.burial_plot_reference:
                    # Multiple burial plot references in wikidata entries
                    result = None
                    break
        
        return result
    
    def get_values_for_openstreetmap_element(self, openstreetmap_element, wikidata_entries):
        wikimedia_commons_category = self.get_wikimedia_commons_category(openstreetmap_element, wikidata_entries)
        main_image = self.get_main_image(wikimedia_commons_category)
        
        result = {
            'burial_plot_reference': self.get_burial_plot_reference(wikidata_entries),
            'wikimedia_commons_category_id': wikimedia_commons_category.id if wikimedia_commons_category else None,
            'main_image_id': main_image.id if main_image else None,
            'deleted': False,
        }
        
        result.update(self.get_dates(wikidata_entries))
        
        return result
    
    def get_name(self, language, openstreetmap_element, wikidata_fetched_entries):
        result = u''
        
        # Use person localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    if hasattr(wikidata_localized_entry, 'wikipedia_page'):
                        result = wikidata_localized_entry.wikipedia
                    else:
                        result = wikidata_localized_entry.name
        
        # Use none-type localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.NO_TYPE:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    if hasattr(wikidata_localized_entry, 'wikipedia_page'):
                        result = wikidata_localized_entry.wikipedia
                    else:
                        result = wikidata_localized_entry.name
        
        # Use OpenStreetMap if language match
        if not result and language.code == self.openstreetmap_name_tag_language:
            result = openstreetmap_element.name
        
        # Concatenate names of person wikidata entries
        if not result:
            error = False
            person_localized_entries = []
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                    wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    wikidata_localized_entry = wikidata_entry.localizations.filter(language=language).first()
                    if wikidata_localized_entry and (wikidata_localized_entry.name or wikidata_localized_entry.wikipedia):
                        person_localized_entries.append(wikidata_localized_entry)
                    else:
                        # No localization or no name for this entry
                        error = True
                        break
            if person_localized_entries:
                sorted_list = sorted(person_localized_entries, key=lambda wikidata_localized_entry: wikidata_localized_entry.wikipedia_page.default_sort if hasattr(wikidata_localized_entry, 'wikipedia_page') and wikidata_localized_entry.wikipedia_page.default_sort else (wikidata_localized_entry.wikipedia if wikidata_localized_entry.wikipedia else wikidata_localized_entry.name))
                
                sorted_list_names = [entry.wikipedia if entry.wikipedia else entry.name for entry in sorted_list]
                last_part = language.last_enumeration_separator.join(sorted_list_names[-2:])
                sorted_list_names[-2:] = [last_part]
                result = language.enumeration_separator.join(sorted_list_names)
        
        # Use OpenStreetMap
        if not result:
            result = openstreetmap_element.name
        
        return result
    
    def get_sorting_name(self, language, name, openstreetmap_element, wikidata_fetched_entries):
        result = u''
        
        # Use person localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    if hasattr(wikidata_localized_entry, 'wikipedia_page'):
                        result = wikidata_localized_entry.wikipedia_page.default_sort
        
        if not result.split(',')[0] in name:
            result = u''
        
        # Use none-type localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.NO_TYPE:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    if hasattr(wikidata_localized_entry, 'wikipedia_page'):
                        result = wikidata_localized_entry.wikipedia_page.default_sort
        
        if not result.split(',')[0] in name:
            result = u''
        
        # Use first default_sort of list of person contained in name
        if not result:
            error = False
            person_wikipedia_pages = []
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                    wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    wikidata_localized_entry = wikidata_entry.localizations.filter(language=language).first()
                    if wikidata_localized_entry and hasattr(wikidata_localized_entry, 'wikipedia_page') and wikidata_localized_entry.wikipedia_page.default_sort:
                        person_wikipedia_pages.append(wikidata_localized_entry.wikipedia_page)
                    else:
                        # No localization or no name for this entry
                        error = True
                        break
            if person_wikipedia_pages:
                sorted_list = sorted(person_wikipedia_pages, key=lambda wikipedia_page: wikipedia_page.default_sort)
                
                for wikipedia_page in sorted_list:
                    if wikipedia_page.default_sort.split(',')[0] in name:
                        result = wikipedia_page.default_sort
                        break
        
        if not result.split(',')[0] in name:
            result = u''
        
        # Use OpenStreetMap
        if not result:
            result = openstreetmap_element.sorting_name
        
        if not result.split(',')[0] in name:
            result = name
        
        return result
    
    def get_description(self, language, openstreetmap_element, wikidata_fetched_entries):
        result = u''
        
        # Use person localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.PERSON:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    result = wikidata_localized_entry.description
        
        # Use none-type localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.NO_TYPE:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry:
                    result = wikidata_localized_entry.description
        
        # Use artist localized wikidata entry if unique
        if not result:
            unique_wikidata_entry = None
            for wikidata_fetched_entry in wikidata_fetched_entries:
                if wikidata_fetched_entry.split(':')[0] == SuperLachaiseWikidataRelation.ARTIST:
                    if not unique_wikidata_entry:
                        unique_wikidata_entry = WikidataEntry.objects.get(wikidata_id=wikidata_fetched_entry.split(':')[-1])
                    else:
                        unique_wikidata_entry = None
                        break
            if unique_wikidata_entry:
                wikidata_localized_entry = unique_wikidata_entry.localizations.filter(language=language).first()
                if wikidata_localized_entry and wikidata_localized_entry.name:
                    result = language.artist_prefix + wikidata_localized_entry.name
        
        return result
    
    def get_localized_values_for_openstreetmap_element(self, language, openstreetmap_element, wikidata_entries):
        name = self.get_name(language, openstreetmap_element, wikidata_entries)
        result = {
            'name': name,
            'sorting_name': self.get_sorting_name(language, name, openstreetmap_element, wikidata_entries),
            'description': self.get_description(language, openstreetmap_element, wikidata_entries),
        }
        
        return result
    
    def sync_superlachaise_wikidata_relation(self, openstreetmap_element_id, relation_type, wikidata_id):
        target_object_id_dict = {"superlachaise_poi__openstreetmap_element__openstreetmap_id": openstreetmap_element_id, "wikidata_entry__wikidata_id": wikidata_id, "relation_type": relation_type}
        
        # Get element in database if it exists
        wikidata_relation = SuperLachaiseWikidataRelation.objects.filter(**target_object_id_dict).first()
        
        if not wikidata_relation:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseWikidataRelation", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pendingModification.pk)
            
            pendingModification.action = PendingModification.CREATE_OR_UPDATE
            pendingModification.modified_fields = u''
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.fetched_wikidata_relations_pks.append(wikidata_relation.pk)
            
            # Delete the previous modification if any
            pendingModification = PendingModification.objects.filter(target_object_class="SuperLachaiseWikidataRelation", target_object_id=json.dumps(target_object_id_dict)).delete()
    
    def sync_superlachaise_category_relation(self, openstreetmap_element_id, category_code):
        target_object_id_dict = {"superlachaise_poi__openstreetmap_element__openstreetmap_id": openstreetmap_element_id, "superlachaise_category__code": category_code}
        
        # Get element in database if it exists
        category_relation = SuperLachaiseCategoryRelation.objects.filter(**target_object_id_dict).first()
        
        if not category_relation:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseCategoryRelation", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pendingModification.pk)
            
            pendingModification.action = PendingModification.CREATE_OR_UPDATE
            pendingModification.modified_fields = u''
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.fetched_category_relations_pks.append(category_relation.pk)
            
            # Delete the previous modification if any
            pendingModification = PendingModification.objects.filter(target_object_class="SuperLachaiseCategoryRelation", target_object_id=json.dumps(target_object_id_dict)).delete()
    
    def sync_superlachaise_localized_poi(self, openstreetmap_element_id, language_code, values_dict):
        target_object_id_dict = {"superlachaise_poi__openstreetmap_element__openstreetmap_id": openstreetmap_element_id, "language__code": language_code}
        
        # Get element in database if it exists
        superlachaise_localized_poi = SuperLachaiseLocalizedPOI.objects.filter(**target_object_id_dict).first()
        
        if not superlachaise_localized_poi:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseLocalizedPOI", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pendingModification.pk)
            
            pendingModification.action = PendingModification.CREATE_OR_UPDATE
            pendingModification.modified_fields = json.dumps(values_dict)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.localized_fetched_objects_pks.append(superlachaise_localized_poi.pk)
            
            # Search for modifications
            modified_values = {}
            
            for field, value in values_dict.iteritems():
                if value != getattr(superlachaise_localized_poi, field):
                    modified_values[field] = value
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseLocalizedPOI", target_object_id=json.dumps(target_object_id_dict))
                self.fetched_pending_modifications_pks.append(pendingModification.pk)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = PendingModification.CREATE_OR_UPDATE
                
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="SuperLachaiseLocalizedPOI", target_object_id=json.dumps(target_object_id_dict)).delete()
    
    def sync_superlachaise_poi(self, openstreetmap_element_id):
        target_object_id_dict = {"openstreetmap_element__openstreetmap_id": openstreetmap_element_id}
        
        openstreetmap_element = OpenStreetMapElement.objects.get(openstreetmap_id=openstreetmap_element_id)
        
        wikidata_entries = self.get_wikidata_entries(openstreetmap_element)
        values_dict = self.get_values_for_openstreetmap_element(openstreetmap_element, wikidata_entries)
        
        # Get element in database if it exists
        superlachaise_poi = SuperLachaisePOI.objects.filter(**target_object_id_dict).first()
        
        if not superlachaise_poi:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pendingModification.pk)
            
            pendingModification.action = PendingModification.CREATE_OR_UPDATE
            pendingModification.modified_fields = json.dumps(values_dict, default=date_handler)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.fetched_objects_pks.append(superlachaise_poi.pk)
            
            # Search for modifications
            modified_values = {}
            
            for field, value in values_dict.iteritems():
                if value != getattr(superlachaise_poi, field):
                    modified_values[field] = value
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=json.dumps(target_object_id_dict))
                self.fetched_pending_modifications_pks.append(pendingModification.pk)
                pendingModification.modified_fields = json.dumps(modified_values, default=date_handler)
                pendingModification.action = PendingModification.CREATE_OR_UPDATE
                
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="SuperLachaisePOI", target_object_id=json.dumps(target_object_id_dict)).delete()
        
        for language in Language.objects.all():
            localized_values_dict = self.get_localized_values_for_openstreetmap_element(language, openstreetmap_element, wikidata_entries)
            self.sync_superlachaise_localized_poi(openstreetmap_element_id, language.code, localized_values_dict)
        
        for wikidata_entry in wikidata_entries:
            wikidata_entry_split = wikidata_entry.split(':')
            self.sync_superlachaise_wikidata_relation(openstreetmap_element_id, wikidata_entry_split[0], wikidata_entry_split[1])
        
        for superlachaise_category_code in self.get_superlachaise_categories(openstreetmap_element, wikidata_entries):
            self.sync_superlachaise_category_relation(openstreetmap_element_id, superlachaise_category_code)
    
    def sync_superlachaise_pois(self, param_openstreetmap_element_ids):
        # Get OpenStreetMap elements
        if param_openstreetmap_element_ids:
            openstreetmap_element_ids = param_openstreetmap_element_ids.split('|')
        else:
            openstreetmap_element_ids = []
            for openstreetmap_element in OpenStreetMapElement.objects.filter(deleted=False):
                openstreetmap_element_ids.append(openstreetmap_element.openstreetmap_id)
        
        self.fetched_objects_pks = []
        self.localized_fetched_objects_pks = []
        self.fetched_wikidata_relations_pks = []
        self.fetched_category_relations_pks = []
        self.fetched_pending_modifications_pks = []
        
        print_unicode(_('Preparing objects...'))
        total = len(openstreetmap_element_ids)
        count = 0
        max_count_per_request = 25
        for chunk in [openstreetmap_element_ids[i:i+max_count_per_request] for i in range(0,len(openstreetmap_element_ids),max_count_per_request)]:
            print_unicode(str(count) + u'/' + str(total))
            count += len(chunk)
            
            for openstreetmap_element_id in chunk:
                self.sync_superlachaise_poi(openstreetmap_element_id)
        print_unicode(str(count) + u'/' + str(total))
        
        if not param_openstreetmap_element_ids:
            # Delete pending creations if element was not fetched
            PendingModification.objects.filter(target_object_class="SuperLachaisePOI", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
            PendingModification.objects.filter(target_object_class="SuperLachaiseLocalizedPOI", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
            PendingModification.objects.filter(target_object_class="SuperLachaiseWikidataRelation", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
            PendingModification.objects.filter(target_object_class="SuperLachaiseCategoryRelation", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
            
            # Look for deleted elements
            for superlachaise_poi in SuperLachaisePOI.objects.filter(deleted=False).exclude(pk__in=self.fetched_objects_pks):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaisePOI", target_object_id=json.dumps({"openstreetmap_element__openstreetmap_id": superlachaise_poi.openstreetmap_element.openstreetmap_id}))
                
                pendingModification.action = PendingModification.CREATE_OR_UPDATE
                pendingModification.modified_fields = json.dumps({"deleted": True})
                
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            for superlachaise_localized_poi in SuperLachaiseLocalizedPOI.objects.exclude(Q(pk__in=self.localized_fetched_objects_pks) | ~Q(superlachaise_poi__pk__in=self.fetched_objects_pks)):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseLocalizedPOI", target_object_id=json.dumps({"superlachaise_poi__openstreetmap_element__openstreetmap_id": superlachaise_localized_poi.superlachaise_poi.openstreetmap_element.openstreetmap_id, "language__code": superlachaise_localized_poi.language.code}))
                
                pendingModification.action = PendingModification.DELETE
                pendingModification.modified_fields = u''
                
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            for wikidata_relation in SuperLachaiseWikidataRelation.objects.exclude(Q(pk__in=self.fetched_wikidata_relations_pks) | ~Q(superlachaise_poi__pk__in=self.fetched_objects_pks)):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseWikidataRelation", target_object_id=json.dumps({"superlachaise_poi__openstreetmap_element__openstreetmap_id": wikidata_relation.superlachaise_poi.openstreetmap_element.openstreetmap_id, "wikidata_entry__wikidata_id": wikidata_relation.wikidata_entry.wikidata_id, "relation_type": wikidata_relation.relation_type}))
                
                pendingModification.action = PendingModification.DELETE
                pendingModification.modified_fields = u''
                
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            for category_relation in SuperLachaiseCategoryRelation.objects.exclude(Q(pk__in=self.fetched_category_relations_pks) | ~Q(superlachaise_poi__pk__in=self.fetched_objects_pks)):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="SuperLachaiseCategoryRelation", target_object_id=json.dumps({"superlachaise_poi__openstreetmap_element__openstreetmap_id": category_relation.superlachaise_poi.openstreetmap_element.openstreetmap_id, "superlachaise_category__code": category_relation.superlachaise_category.code}))
                
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
        
        try:
            self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0].split('sync_')[-1])
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.auto_apply = (Setting.objects.get(key=u'superlachaise_poi:auto_apply_modifications').value == 'true')
            self.openstreetmap_name_tag_language = Setting.objects.get(key=u'openstreetmap:name_tag_language').value
            self.synced_instance_of = json.loads(Setting.objects.get(key=u'wikimedia_commons:synced_instance_of').value)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            self.sync_superlachaise_pois(options['openstreetmap_element_ids'])
            print_unicode(_('== End %s ==') % self.synchronization.name)
            
            self.synchronization.created_objects = self.created_objects
            self.synchronization.modified_objects = self.modified_objects
            self.synchronization.deleted_objects = self.deleted_objects
            self.synchronization.errors = ', '.join(self.errors)
            
            translation.deactivate()
        except:
            print_unicode(traceback.format_exc())
            error = sys.exc_info()[1]
            self.synchronization.errors = traceback.format_exc()
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        if error:
            raise CommandError(error)
