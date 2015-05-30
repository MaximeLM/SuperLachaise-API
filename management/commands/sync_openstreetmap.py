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

import json, math, overpy, sys, traceback
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
                
                modified_fields = json.loads(pendingModification.modified_fields) if pendingModification.modified_fields else {}
                for key in values_dict:
                    modified_fields.pop(key, None)
                modified_fields.update(modified_values)
                pendingModification.modified_fields = json.dumps(modified_fields, default=decimal_handler)
                pendingModification.action = "modify"
                
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="OpenStreetMapElement", target_object_id=str(overpass_element.id)).first()
                if pendingModification:
                    modified_fields = json.loads(pendingModification.modified_fields) if pendingModification.modified_fields else {}
                    for key in values_dict:
                        modified_fields.pop(key, None)
                    if not modified_fields:
                        pendingModification.delete()
                
    
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
        result = self.download_data(self.bounding_box)
        
        # Handle downloaded elements
        fetched_ids = []
        for element in result.nodes:
            if self.element_accepted(element):
                fetched_ids.append(element.id)
                self.handle_element(element, {'x': element.lat, 'y': element.lon})
        for element in result.ways:
            if self.element_accepted(element):
                fetched_ids.append(element.id)
                self.handle_way(element)
        for element in result.relations:
            if self.element_accepted(element):
                fetched_ids.append(element.id)
                self.handle_relation(element)
        
        # Delete pending creations if element was deleted in OSM
        for pendingModification in PendingModification.objects.filter(target_object_class="OpenStreetMapElement", action=PendingModification.CREATE):
            if not long(pendingModification.target_object_id) in fetched_ids:
                pendingModification.delete()
        
        # Look for deleted elements
        for openStreetMap_element in OpenStreetMapElement.objects.all():
            if not long(openStreetMap_element.id) in fetched_ids:
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
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(category='OpenStreetMap', key=u'auto_apply_modifications').value == 'true')
            self.bounding_box = Setting.objects.get(category='OpenStreetMap', key=u'bounding_box').value
            self.exclude_ids = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'exclude_ids').value)
            self.synced_tags = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'synced_tags').value)
        
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_openstreetmap()
            
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
