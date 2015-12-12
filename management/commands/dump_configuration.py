# -*- coding: utf-8 -*-

"""
dump_configuration.py
superlachaise_api

Created by Maxime Le Moine on 14/06/2015.
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

import json, os
from django.core.management.base import BaseCommand, CommandError

from superlachaise_api.models import *

configuration_models = {
    Synchronization: {
        'id_fields': ['name'],
        'other_fields': ['dependency_order'],
    },
    LocalizedSynchronization: {
        'id_fields': ['synchronization__name', 'language__code'],
        'other_fields': ['description'],
    },
    Language: {
        'id_fields': ['code'],
        'other_fields': ['description', 'enumeration_separator', 'last_enumeration_separator', 'artist_prefix'],
    },
    Setting: {
        'id_fields': ['key'],
        'other_fields': ['default'],
    },
    LocalizedSetting: {
        'id_fields': ['setting__key', 'language__code'],
        'other_fields': ['description'],
    },
    SuperLachaiseCategory: {
        'id_fields': ['code'],
        'other_fields': ['type', 'values'],
    },
    SuperLachaiseLocalizedCategory: {
        'id_fields': ['superlachaise_category__code', 'language__code'],
        'other_fields': ['name'],
    },
    WikidataOccupation: {
        'id_fields': ['wikidata_id'],
        'other_fields': ['name', 'superlachaise_category__code'],
    },
}

class Command(BaseCommand):
    
    def resolve_field_relation(self, object, field):
        if len(field.split('__')) == 2:
            resolved_field = field.split('__')[0]
            value = getattr(object, resolved_field)
            if value:
                result = getattr(value, field.split('__')[1])
            else:
                result = None
        else:
            result = getattr(object, field)
        return result
    
    def handle(self, *args, **options):
        result = {}
        for model, fields in configuration_models.iteritems():
            objects_dicts = []
            for object in model.objects.all():
                object_dict = {}
                for field in fields['id_fields']:
                    object_dict[field] = self.resolve_field_relation(object, field)
                for field in fields['other_fields']:
                    object_dict[field] = self.resolve_field_relation(object, field)
                
                objects_dicts.append(object_dict)
            result[model.__name__] = objects_dicts
        
        with open(os.path.dirname(__file__) + '/../../configuration/configuration.json', 'w') as configuration_file:
            configuration_file.write(json.dumps(result, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True).encode('utf8'))
