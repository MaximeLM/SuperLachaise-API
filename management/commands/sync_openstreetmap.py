# -*- coding: utf-8 -*-

"""
sync_openstreetmap.py
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

import json, math, os, overpy, requests, sys, traceback
from decimal import Decimal
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def decimal_handler(obj):
    return str(obj) if isinstance(obj, Decimal) else obj

def area_for_polygon(polygon):
    result = 0
    imax = len(polygon) - 1
    for i in range(0,imax):
        result += (polygon[i]['x'] * polygon[i+1]['y']) - (polygon[i+1]['x'] * polygon[i]['y'])
    result += (polygon[imax]['x'] * polygon[0]['y']) - (polygon[0]['x'] * polygon[imax]['y'])
    return result / 2.

def centroid_for_polygon(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) - 1
    
    result_x = 0
    result_y = 0
    for i in range(0,imax):
        result_x += (polygon[i]['x'] + polygon[i+1]['x']) * ((polygon[i]['x'] * polygon[i+1]['y']) - (polygon[i+1]['x'] * polygon[i]['y']))
        result_y += (polygon[i]['y'] + polygon[i+1]['y']) * ((polygon[i]['x'] * polygon[i+1]['y']) - (polygon[i+1]['x'] * polygon[i]['y']))
    result_x += (polygon[imax]['x'] + polygon[0]['x']) * ((polygon[imax]['x'] * polygon[0]['y']) - (polygon[0]['x'] * polygon[imax]['y']))
    result_y += (polygon[imax]['y'] + polygon[0]['y']) * ((polygon[imax]['x'] * polygon[0]['y']) - (polygon[0]['x'] * polygon[imax]['y']))
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)
    
    return {'x': result_x, 'y': result_y}

def none_to_blank(s):
    if s is None:
        return u''
    return unicode(s)

class Command(BaseCommand):
    
    def request_wikidata_with_wikipedia_links(self, language_code, wikipedia_links):
        result = {}
        last_continue = {
            'continue': '',
        }
        languages = Language.objects.all().values_list('code', flat=True)
        titles = '|'.join(wikipedia_links).encode('utf8')
        sites = language_code + 'wiki'
        
        while True:
            # Request properties
            params = {
                'languages': languages,
                'action': 'wbgetentities',
                'props': 'sitelinks',
                'format': 'json',
                'sites': sites,
                'titles': titles,
            }
            params.update(last_continue)
            
            if settings.USER_AGENT:
                headers = {"User-Agent" : settings.USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://www.wikidata.org/w/api.php', params=params, headers=headers).json()
            
            if 'entities' in json_result:
                result.update(json_result['entities'])
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return result
    
    def get_wikipedia(self, entity, language_code):
        try:
            wikipedia = entity['sitelinks'][language_code + 'wiki']
            
            return wikipedia['title']
        except:
            return None
    
    def download_data(self, bounding_box):
        query_string_list = ['(\n']
        for synced_tag in self.synced_tags:
            query_string_list.append(""\
                "\tnode[{tag}]({bounding_box});\n" \
                "\tway[{tag}]({bounding_box});\n" \
                "\trelation[{tag}]({bounding_box});\n".format(tag=synced_tag, bounding_box=bounding_box)
                )
        query_string_list.append(');\n(._;>;);out body;')
        query_string = "".join(query_string_list)
        
        api = overpy.Overpass()
        result = api.query(query_string)
        
        return result
    
    def get_wiki_values(self, overpass_element, field_name):
        result = []
        for key, value in {key:value for (key,value) in overpass_element.tags.iteritems() if field_name in key}.iteritems():
            wiki_value = []
            for key_part in key.split(':'):
                if not key_part == field_name:
                    wiki_value.append(key_part)
            
            value_field = value
            if len(value_field.split(':')) == 2:
                # fr:foo;bar
                wiki_value.append(value.split(':')[0])
                value_field = value.split(':')[1]
            
            for sub_value in value_field.split(';'):
                sub_list = list(wiki_value)
                sub_list.extend(sub_value.split(':'))
                result.append(':'.join(sub_list))
        
        return ';'.join(result)
    
    def get_nature(self, overpass_element):
        return overpass_element.tags.get("historic")
    
    def get_values_from_element(self, overpass_element, coordinate):
        result = {
            'type': overpass_element.__class__.__name__.lower(),
            'name': none_to_blank(overpass_element.tags.get("name")),
            'sorting_name': overpass_element.tags.get("sorting_name"),
            'latitude': coordinate['x'],
            'longitude': coordinate['y'],
            'wikipedia': none_to_blank(self.get_wiki_values(overpass_element, 'wikipedia')),
            'wikidata': none_to_blank(self.get_wiki_values(overpass_element, 'wikidata')),
            'wikimedia_commons': none_to_blank(overpass_element.tags.get("wikimedia_commons")),
        }
        
        result['nature'] = self.get_nature(overpass_element)
        
        # Get combined wikidata field
        wikidata_combined = []
        
        if result['wikipedia']:
            for wikipedia in result['wikipedia'].split(';'):
                if ':' in wikipedia:
                    language_code = wikipedia.split(':')[-2]
                    link = wikipedia.split(':')[-1]
                    if language_code in self.wikidata_codes and link in self.wikidata_codes[language_code]:
                        wikidata_code = self.wikidata_codes[language_code][link]
                        wikidata_link = wikipedia.split(language_code + u':' + link)[0] + wikidata_code
                        if not wikidata_link in wikidata_combined:
                            wikidata_combined.append(wikidata_link)
                    else:
                        self.errors = self.errors + 1
                        admin_command_error = AdminCommandError(admin_command=self.admin_command, type=_('wikipedia page not found'))
                        admin_command_error.description = _("A wikipedia page of an OpenStreetMap element could not be found.")
                        admin_command_error.target_object_class = "OpenStreetMapElement"
                        admin_command_error.target_object_id = overpass_element.id

                        admin_command_error.full_clean()
                        admin_command_error.save()
        
        if result['wikidata']:
            for wikidata_link in result['wikidata'].split(';'):
                if not wikidata_link in wikidata_combined:
                    wikidata_combined.append(wikidata_link)
        
        wikidata_combined.sort()
        result['wikidata_combined'] = ';'.join(wikidata_combined)
        
        if not result['sorting_name']:
            result['sorting_name'] = result['name']
        
        return result
    
    def handle_element(self, overpass_element, coordinate):
        # Get element in database if it exists
        openStreetMap_element = OpenStreetMapElement.objects.filter(id=overpass_element.id).first()
        
        if not openStreetMap_element:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapElement", target_object_id=str(overpass_element.id))
            
            values_dict = self.get_values_from_element(overpass_element, coordinate)
            
            pendingModification.action = "create"
            pendingModification.modified_fields = json.dumps(values_dict, default=decimal_handler)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            # Search for modifications
            modified_values = {}
            
            values_dict = self.get_values_from_element(overpass_element, coordinate)
            for field, value in values_dict.iteritems():
                if value != getattr(openStreetMap_element, field):
                    modified_values[field] = value
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapElement", target_object_id=str(overpass_element.id))
                
                pendingModification.modified_fields = json.dumps(modified_values, default=decimal_handler)
                pendingModification.action = "modify"
                
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                PendingModification.objects.filter(target_object_class="OpenStreetMapElement", target_object_id=str(overpass_element.id)).delete()
    
    def handle_way(self, overpass_way):
        # Get way centroid
        polygon = []
        for node in overpass_way.nodes:
            polygon.append({'x': float(node.lat), 'y': float(node.lon)})
        centroid = centroid_for_polygon(polygon)
        coordinate = {'x': Decimal(centroid['x']).quantize(Decimal('.0000001')), 'y': Decimal(centroid['y']).quantize(Decimal('.0000001'))}
        
        # Handle element
        self.handle_element(overpass_way, coordinate)
    
    def handle_relation(self, overpass_relation):
        # Search for outer way
        outer_way = None
        for member in overpass_relation.members:
            if member.role == 'outer' and member.__class__.__name__ == 'RelationWay':
                outer_way = member
                break
        
        if outer_way:
            # Get outer way centroid
            polygon = []
            for node in member.resolve().nodes:
                polygon.append({'x': float(node.lat), 'y': float(node.lon)})
            centroid = centroid_for_polygon(polygon)
            coordinate = {'x': Decimal(centroid['x']).quantize(Decimal('.0000001')), 'y': Decimal(centroid['y']).quantize(Decimal('.0000001'))}
            
            # Handle element
            self.handle_element(overpass_relation, coordinate)
        else:
            raise Exception(_('no outer way for relation found'))
    
    def element_accepted(self, element):
        result = False
        
        # Check if tag is explicitky excluded
        for excluded_id in self.exclude_ids:
            if excluded_id['type'] == element.__class__.__name__.lower() and excluded_id['id'] == element.id:
                return False
        
        # Check if tag is to be synced
        for synced_tag in self.synced_tags:
            tag_splitted = synced_tag.split("=")
            if element.tags.get(tag_splitted[0]) == tag_splitted[1]:
                result = True
                break
        
        return result
    
    def sync_openstreetmap(self):
        # Download data from OSM
        print 'Requesting Overpass API...'
        result = self.download_data(self.bounding_box)
        
        wikipedia_to_fetch = {}
        self.wikidata_codes = {}
        for element_type in [result.nodes, result.ways, result.relations]:
            for element in element_type:
                wikipedias = self.get_wiki_values(element, 'wikipedia')
                for wikipedia in wikipedias.split(';'):
                    if ':' in wikipedia:
                        language_code = wikipedia.split(':')[-2]
                        link = wikipedia.split(':')[-1]
                        if not language_code in wikipedia_to_fetch:
                            wikipedia_to_fetch[language_code] = []
                        if not link in wikipedia_to_fetch[language_code]:
                            wikipedia_to_fetch[language_code].append(link)
        print 'Requesting Wikidata...'
        total = 0
        for language, wikipedia_links in wikipedia_to_fetch.iteritems():
            total += len(wikipedia_links)
        count = 0
        max_count_per_request = 25
        for language_code, wikipedia_links in wikipedia_to_fetch.iteritems():
            self.wikidata_codes[language_code] = {}
            wikipedia_links = list(set(wikipedia_links))
            for chunk in [wikipedia_links[i:i+max_count_per_request] for i in range(0,len(wikipedia_links),max_count_per_request)]:
                print str(count) + u'/' + str(total)
                count += len(chunk)
                
                entities = self.request_wikidata_with_wikipedia_links(language_code, chunk)
                for wikidata_code, entity in entities.iteritems():
                    wikipedia = self.get_wikipedia(entity, language_code)
                    self.wikidata_codes[language_code][wikipedia] = wikidata_code
        print str(count) + u'/' + str(total)
        
        # Handle downloaded elements
        fetched_ids = []
        for element in result.nodes:
            if self.element_accepted(element):
                fetched_ids.append(str(element.id))
                self.handle_element(element, {'x': element.lat, 'y': element.lon})
        for element in result.ways:
            if self.element_accepted(element):
                fetched_ids.append(str(element.id))
                self.handle_way(element)
        for element in result.relations:
            if self.element_accepted(element):
                fetched_ids.append(str(element.id))
                self.handle_relation(element)
        
        # Delete pending creations if element was deleted in OSM
        PendingModification.objects.filter(target_object_class="OpenStreetMapElement", action=PendingModification.CREATE).exclude(target_object_id__in=fetched_ids).delete()
        
        # Look for deleted elements
        for openStreetMap_element in OpenStreetMapElement.objects.exclude(id__in=fetched_ids):
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapElement", target_object_id=openStreetMap_element.id)
            
            pendingModification.action = PendingModification.DELETE
            pendingModification.modified_fields = u''
            
            pendingModification.full_clean()
            pendingModification.save()
            self.deleted_objects = self.deleted_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        self.admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(key=u'openstreetmap:auto_apply_modifications').value == 'true')
            self.bounding_box = Setting.objects.get(key=u'openstreetmap:bounding_box').value
            self.exclude_ids = json.loads(Setting.objects.get(key=u'openstreetmap:exclude_ids').value)
            self.synced_tags = json.loads(Setting.objects.get(key=u'openstreetmap:synced_tags').value)
        
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = 0
            
            self.sync_openstreetmap()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.deleted_objects > 0:
                result_list.append(_('{nb} object(s) deleted').format(nb=self.deleted_objects))
            if self.errors > 0:
                result_list.append(_('{nb} error(s)').format(nb=self.errors))
            
            if result_list:
                self.admin_command.last_result = ', '.join(result_list)
            else:
                self.admin_command.last_result = _("No modifications")
        except:
            exception = sys.exc_info()[0]
            self.admin_command.last_result = exception.__class__.__name__ + ': ' + traceback.format_exc()
        
        self.admin_command.last_executed = timezone.now()
        self.admin_command.save()
        
        translation.deactivate()
