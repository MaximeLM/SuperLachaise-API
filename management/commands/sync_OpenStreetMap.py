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

import overpy, traceback
import os, json, math, sys
from decimal import *
import xml.etree.ElementTree as ET
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

def xstr(s):
    if s is None:
        return u''
    return unicode(s)

class Command(BaseCommand):
    
    created_POIs = 0
    modified_POIs = 0
    deleted_POIs = 0
    
    def download_data(self, bounding_box):
        api = overpy.Overpass()
        synced_tags = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'synced_tags').value)
    
        query_string_list = ['(\n']
        for synced_tag in synced_tags:
            query_string_list.append(""\
                "\tnode[{tag}]({bounding_box});\n" \
                "\tway[{tag}]({bounding_box});\n" \
                "\trelation[{tag}]({bounding_box});\n".format(tag=synced_tag, bounding_box=bounding_box)
                )
        query_string_list.append(');\n(._;>;);out body;')
    
        query_string = "".join(query_string_list)
    
        result = api.query(query_string)
    
        return result

    def handle_POI(self, overpass_POI, coordinate):
        auto_apply = (Setting.objects.get(category='Modifications', key=u'auto_apply').value == 'true')
    
        openStreetMap_POI = OpenStreetMapPOI.objects.filter(id=overpass_POI.id).first()
    
        if openStreetMap_POI:
            modified_values = {}
            type = overpass_POI.__class__.__name__.lower()
            if xstr(type) != openStreetMap_POI.type:
                modified_values['type'] = type
            name = overpass_POI.tags.get("name")
            if xstr(name) != openStreetMap_POI.name:
                modified_values['name'] = name
            historic = overpass_POI.tags.get("historic")
            if xstr(historic) != openStreetMap_POI.historic:
                modified_values['historic'] = historic
            wikipedia = overpass_POI.tags.get("wikipedia")
            if xstr(wikipedia) != openStreetMap_POI.wikipedia:
                modified_values['wikipedia'] = wikipedia
            wikidata = overpass_POI.tags.get("wikidata")
            if xstr(wikidata) != openStreetMap_POI.wikidata:
                modified_values['wikidata'] = wikidata
            wikimedia_commons = overpass_POI.tags.get("wikimedia_commons")
            if xstr(wikimedia_commons) != openStreetMap_POI.wikimedia_commons:
                modified_values['wikimedia_commons'] = wikimedia_commons
            latitude = coordinate['x']
            if latitude != openStreetMap_POI.latitude:
                modified_values['latitude'] = str(latitude)
            longitude = coordinate['y']
            if longitude != openStreetMap_POI.longitude:
                modified_values['longitude'] = str(longitude)
        
            if modified_values:
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = "modify"
                
                try:
                    pendingModification.full_clean()
                    pendingModification.save()
                    self.modified_POIs = self.modified_POIs + 1
                except Exception as exception:
                    print exception
            
                if auto_apply:
                    pendingModification.apply_modification()
            else:
                pendingModification = PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id).first()
                if pendingModification:
                    pendingModification.delete()
        
        else:
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id)
        
            modified_fields_dict = { 'type': overpass_POI.__class__.__name__.lower(),
                                'name': overpass_POI.tags.get("name"),
                                'latitude': str(coordinate['x']),
                                'longitude': str(coordinate['y']),
                                'historic': overpass_POI.tags.get("historic"),
                                'wikipedia': overpass_POI.tags.get("wikipedia"),
                                'wikidata': overpass_POI.tags.get("wikidata"),
                                'wikimedia_commons': overpass_POI.tags.get("wikimedia_commons"),
                                }
        
            pendingModification.action = "create"
            pendingModification.modified_fields = json.dumps(modified_fields_dict)
            try:
                pendingModification.full_clean()
                pendingModification.save()
                self.created_POIs = self.created_POIs + 1
            except Exception as exception:
                print exception
        
            if auto_apply:
                pendingModification.apply_modification()

    def handle_way(self, overpass_way):
        polygon = []
        for node in overpass_way.nodes:
            polygon.append({'x': float(node.lat), 'y': float(node.lon)})
        centroid = centroid_for_polygon(polygon)
        coordinate = {'x': Decimal(centroid['x']).quantize(Decimal('.0000001')), 'y': Decimal(centroid['y']).quantize(Decimal('.0000001'))}
        self.handle_POI(overpass_way, coordinate)

    def handle_relation(self, overpass_relation):
        ok = False
        for member in overpass_relation.members:
            if member.role == 'outer' and member.__class__.__name__ == 'RelationWay':
                if not ok:
                    ok = True
                    polygon = []
                    for node in member.resolve().nodes:
                        polygon.append({'x': float(node.lat), 'y': float(node.lon)})
                    centroid = centroid_for_polygon(polygon)
                    coordinate = {'x': Decimal(centroid['x']).quantize(Decimal('.0000001')), 'y': Decimal(centroid['y']).quantize(Decimal('.0000001'))}
                    self.handle_POI(overpass_relation, coordinate)
                else:
                    raise Exception('more than one outer way for relation found')
        if ok:
            None
        else:
            raise Exception('no outer way for relation found')

    def fetch_data_OSM(self, use_file):
        auto_apply = (Setting.objects.get(category='Modifications', key=u'auto_apply').value == 'true')
    
        if not use_file:
            bounding_box = Setting.objects.get(category='OpenStreetMap', key=u'bounding_box').value
            result = self.download_data(bounding_box)
        else:
            tree = ET.parse(os.path.dirname(os.path.realpath(__file__)) + '/sync_OpenStreetMap.osm')
            result = overpy.Result.from_xml(tree.getroot())
    
        fetched_ids = []
        exclude_ids = json.loads(Setting.objects.get(category='OpenStreetMap', key=u'exclude_ids').value)
    
        for POI in result.nodes:
            if POI.tags.get("historic") in ['tomb', 'memorial'] and not POI.id in exclude_ids:
                fetched_ids.append(POI.id)
                self.handle_POI(POI, {'x': POI.lat, 'y': POI.lon})
        for POI in result.ways:
            if POI.tags.get("historic") in ['tomb', 'memorial'] and not POI.id in exclude_ids:
                fetched_ids.append(POI.id)
                self.handle_way(POI)
        for POI in result.relations:
            if POI.tags.get("historic") in ['tomb', 'memorial'] and not POI.id in exclude_ids:
                fetched_ids.append(POI.id)
                self.handle_relation(POI)
    
        for pendingModification in PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", action="create"):
            if not pendingModification.target_object_id in fetched_ids:
                pendingModification.delete()
    
        for openStreetMap_POI in OpenStreetMapPOI.objects.all():
            if not openStreetMap_POI.id in fetched_ids:
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=openStreetMap_POI.id)
            
                pendingModification.action = "delete"
                pendingModification.modified_fields = ''
                pendingModification.save()
                self.deleted_POIs = self.deleted_POIs + 1
            
                if auto_apply:
                    pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--use_file',
            action='store_true',
            dest='use_file',
            default=False)
    
    def handle(self, *args, **options):
        admin_command = AdminCommand.objects.get(name='sync_OpenStreetMap')
        
        self.created_POIs = 0
        self.modified_POIs = 0
        self.deleted_POIs = 0
        
        try:
            self.fetch_data_OSM(options['use_file'])
            
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
