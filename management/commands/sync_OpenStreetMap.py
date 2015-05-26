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

import json, math, overpy, sys, traceback
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from superlachaise_api.models import Setting, OpenStreetMapPOI, PendingModification, AdminCommand

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
    
    created_POIs = 0
    modified_POIs = 0
    deleted_POIs = 0
    
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
    
    def handle_element(self, overpass_element, coordinate):
        # Get POI in database if it exists
        openStreetMap_POI = OpenStreetMapPOI.objects.filter(id=overpass_element.id).first()
        
        if openStreetMap_POI:
            # Search for modifications
            modified_values = {}
            type = overpass_element.__class__.__name__.lower()
            if none_to_blank(type) != openStreetMap_POI.type:
                modified_values['type'] = type
            name = overpass_element.tags.get("name")
            if none_to_blank(name) != openStreetMap_POI.name:
                modified_values['name'] = name
            historic = overpass_element.tags.get("historic")
            if none_to_blank(historic) != openStreetMap_POI.historic:
                modified_values['historic'] = historic
            wikipedia = overpass_element.tags.get("wikipedia")
            if none_to_blank(wikipedia) != openStreetMap_POI.wikipedia:
                modified_values['wikipedia'] = wikipedia
            wikidata = overpass_element.tags.get("wikidata")
            if none_to_blank(wikidata) != openStreetMap_POI.wikidata:
                modified_values['wikidata'] = wikidata
            wikimedia_commons = overpass_element.tags.get("wikimedia_commons")
            if none_to_blank(wikimedia_commons) != openStreetMap_POI.wikimedia_commons:
                modified_values['wikimedia_commons'] = wikimedia_commons
            latitude = coordinate['x']
            if latitude != openStreetMap_POI.latitude:
                modified_values['latitude'] = str(latitude)
            longitude = coordinate['y']
            if longitude != openStreetMap_POI.longitude:
                modified_values['longitude'] = str(longitude)
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_element.id)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = "modify"
                
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_POIs = self.modified_POIs + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", target_object_id=overpass_element.id).first()
                if pendingModification:
                    pendingModification.delete()
        
        else:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_element.id)
            
            modified_fields_dict = { 
                                'type': overpass_element.__class__.__name__.lower(),
                                'name': overpass_element.tags.get("name"),
                                'latitude': str(coordinate['x']),
                                'longitude': str(coordinate['y']),
                                'historic': overpass_element.tags.get("historic"),
                                'wikipedia': overpass_element.tags.get("wikipedia"),
                                'wikidata': overpass_element.tags.get("wikidata"),
                                'wikimedia_commons': overpass_element.tags.get("wikimedia_commons"),
                                }
            
            pendingModification.action = "create"
            pendingModification.modified_fields = json.dumps(modified_fields_dict)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_POIs = self.created_POIs + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
    
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
            raise Exception('no outer way for relation found')
    
    def element_accepted(self, element):
        result = False
        for synced_tag in self.synced_tags:
            tag_splitted = synced_tag.split("=")
            if element.tags.get(tag_splitted[0]) == tag_splitted[1]:
                result = True
                break
        return result
    
    def sync_OpenStreetMap(self):
        # Download data from OSM
        result = self.download_data(self.bounding_box)
        
        # Handle downloaded elements
        fetched_ids = []
        for element in result.nodes:
            if self.element_accepted(element) and not element.id in self.exclude_ids:
                fetched_ids.append(element.id)
                self.handle_element(element, {'x': element.lat, 'y': element.lon})
        for element in result.ways:
            if self.element_accepted(element) and not element.id in self.exclude_ids:
                fetched_ids.append(element.id)
                self.handle_way(element)
        for element in result.relations:
            if self.element_accepted(element) and not element.id in self.exclude_ids:
                fetched_ids.append(element.id)
                self.handle_relation(element)
        
        # Delete pending creations if element was deleted in OSM
        for pendingModification in PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", action="create"):
            if not pendingModification.target_object_id in fetched_ids:
                pendingModification.delete()
        
        # Look for deleted elements
        for openStreetMap_POI in OpenStreetMapPOI.objects.all():
            if not openStreetMap_POI.id in fetched_ids:
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=openStreetMap_POI.id)
                
                pendingModification.action = "delete"
                pendingModification.modified_fields = u''
                
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_POIs = self.deleted_POIs + 1
                
                if self.auto_apply:
                    pendingModification.apply_modification()
    
    def handle(self, *args, **options):
        admin_command = AdminCommand.objects.get(name='sync_OpenStreetMap')
        
        self.auto_apply = (Setting.objects.get(category='Modifications', key=u'auto_apply').value == 'true')
        self.bounding_box = Setting.objects.get(category='OpenStreetMap', key=u'bounding_box').value
        self.exclude_ids = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'exclude_ids').value)
        self.synced_tags = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'synced_tags').value)
        
        self.created_POIs = 0
        self.modified_POIs = 0
        self.deleted_POIs = 0
        
        try:
            self.sync_OpenStreetMap()
            
            result_list = []
            if self.created_POIs > 0:
                result_list.append(u'{nb} OpenStreetMap POI(s) created'.format(nb=self.created_POIs))
            if self.modified_POIs > 0:
                result_list.append(u'{nb} OpenStreetMap POI(s) modified'.format(nb=self.modified_POIs))
            if self.deleted_POIs > 0:
                result_list.append(u'{nb} OpenStreetMap POI(s) deleted'.format(nb=self.deleted_POIs))
            
            if result_list:
                admin_command.last_result = ''.join(result_list)
            else:
                admin_command.last_result = u"No modifications"
        except:
            exception = sys.exc_info()[0]
            admin_command.last_result = exception.__class__.__name__ + ': ' + traceback.format_exc()
        
        admin_command.last_executed = timezone.now()
        admin_command.save()
