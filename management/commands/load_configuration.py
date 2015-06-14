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

import importlib, json, os
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        with open(os.path.dirname(__file__) + '/../../configuration/configuration.json', 'r') as configuration_file:
            configuration = json.load(configuration_file)
            
            for model_full_name, objects in configuration.iteritems():
                module = importlib.import_module('.'.join(model_full_name.split('.')[:-1]))
                model = getattr(module, model_full_name.split('.')[-1])
                
                synced_objects = []
                
                for object_fields in objects:
                    if model == AdminCommand:
                        object, created = model.objects.get_or_create(name=object_fields['name'])
                    elif model == Language:
                        object, created = model.objects.get_or_create(code=object_fields['code'])
                    elif model == Setting:
                        object, created = model.objects.get_or_create(key=object_fields['key'])
                    elif model == SuperLachaiseCategory:
                        object, created = model.objects.get_or_create(code=object_fields['code'])
                    elif model == SuperLachaiseLocalizedCategory:
                        object, created = model.objects.get_or_create(language_id=object_fields['language_id'], superlachaise_category_id=object_fields['superlachaise_category_id'])
                    elif model == WikidataOccupation:
                        object, created = model.objects.get_or_create(id=object_fields['id'])
                    else:
                        raise BaseException("Invalid model: %s" % model)
                    
                    for field, value in object_fields.iteritems():
                        setattr(object, field, value)
                    
                    object.save()
                    synced_objects.append(object.pk)
                
                model.objects.exclude(pk__in=synced_objects).delete()
                    
