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

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        models_to_dump = {
            AdminCommand: [
                'name',
                'dependency_order',
            ],
            Language: [
                'code',
                'description',
                'enumeration_separator',
                'last_enumeration_separator',
                'artist_prefix',
            ],
            Setting: [
                'key',
                'value',
            ],
            SuperLachaiseCategory: [
                'code',
                'type',
                'values',
            ],
            SuperLachaiseLocalizedCategory: [
                'language_id',
                'superlachaise_category_id',
                'name',
            ],
            WikidataOccupation: [
                'id',
                'name',
                'superlachaise_category_id',
            ],
        }
        
        result = {}
        for model, fields in models_to_dump.iteritems():
            instances = []
            for object in model.objects.all():
                instance = {}
                for field in fields:
                    instance[field] = getattr(object, field)
                instances.append(instance)
            result[model.__module__ + '.' + model.__name__] = instances
        
        with open(os.path.dirname(__file__) + '/../../configuration/configuration.json', 'w') as configuration_file:
            configuration_file.write(json.dumps(result, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True).encode('utf8'))
