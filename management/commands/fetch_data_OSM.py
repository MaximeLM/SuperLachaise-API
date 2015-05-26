# -*- coding: utf-8 -*-

import overpy
import os, json
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from superlachaise_api.models import Setting, OpenStreetMapPOI, PendingModification, Language

def xstr(s):
    if s is None:
        return u''
    return unicode(s)

def download_data(bounding_box):
    api = overpy.Overpass()
    
    query_string = """
        (node["historic"="memorial"]({{bbox}});
        way["historic"="memorial"]({{bbox}});
        relation["historic"="memorial"]({{bbox}});
        node["historic"="tomb"]({{bbox}});
        way["historic"="tomb"]({{bbox}});
        relation["historic"="tomb"]({{bbox}});
        );(._;>;);
        out body;
        """.replace('{{bbox}}', str(bounding_box))
    
    result = api.query(query_string)
    
    return result

def handle_POI(overpass_POI):
    openStreetMap_POI = OpenStreetMapPOI.objects.filter(id=overpass_POI.id).first()
    
    if openStreetMap_POI:
        modified_values = {}
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
        latitude = overpass_POI.lat
        if latitude != openStreetMap_POI.latitude:
            modified_values['latitude'] = str(latitude)
        longitude = overpass_POI.lon
        if longitude != openStreetMap_POI.longitude:
            modified_values['longitude'] = str(longitude)
        
        if modified_values:
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id)
            pendingModification.new_values = json.dumps(modified_values)
            pendingModification.action = "modify"
            
            try:
                pendingModification.full_clean()
                pendingModification.save()
            except Exception as exception:
                print exception
        else:
            pendingModification = PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id).first()
            if pendingModification:
                pendingModification.delete()
        
    else:
        pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=overpass_POI.id)
        
        new_values_dict = { 'name': overpass_POI.tags.get("name"),
                            'latitude': str(overpass_POI.lat),
                            'longitude': str(overpass_POI.lon),
                            'historic': overpass_POI.tags.get("historic"),
                            'wikipedia': overpass_POI.tags.get("wikipedia"),
                            'wikidata': overpass_POI.tags.get("wikidata"),
                            'wikimedia_commons': overpass_POI.tags.get("wikimedia_commons"),
                            }
        
        pendingModification.action = "create"
        pendingModification.new_values = json.dumps(new_values_dict)
        try:
            pendingModification.full_clean()
            pendingModification.save()
        except Exception as exception:
            print exception

def fetch_data_OSM(use_file):
    if not use_file:
        bounding_box = Setting.objects.get(key=u'OpenStreetMap_bounding_box').value
        result = download_data(bounding_box)
    else:
        tree = ET.parse(os.path.dirname(os.path.realpath(__file__)) + '/fetch_data_OSM.osm')
        result = overpy.Result.from_xml(tree.getroot())
    
    fetched_ids = []
    
    for POI in result.nodes:
        if POI.tags.get("historic") in ['tomb', 'memorial']:
            fetched_ids.append(POI.id)
            handle_POI(POI)
    
    for pendingModification in PendingModification.objects.filter(target_object_class="OpenStreetMapPOI", action="create"):
        if not pendingModification.target_object_id in fetched_ids:
            pendingModification.delete()
    
    for openStreetMap_POI in OpenStreetMapPOI.objects.all():
        if not openStreetMap_POI.id in fetched_ids:
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapPOI", target_object_id=openStreetMap_POI.id)
            
            pendingModification.action = "delete"
            pendingModification.new_values = ''
            pendingModification.save() 

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--use_file',
            action='store_true',
            dest='use_file',
            default=False)
    
    def handle(self, *args, **options):
        fetch_data_OSM(options['use_file'])
