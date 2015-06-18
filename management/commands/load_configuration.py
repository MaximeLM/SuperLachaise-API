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
            
            models = [
                Language,
                Synchronization,
                LocalizedSynchronization,
                Setting,
                LocalizedSetting,
                SuperLachaiseCategory,
                SuperLachaiseLocalizedCategory,
                WikidataOccupation,
            ]
            
            for model in models:
                objects = configuration[model.__name__]
                
                synced_objects = []
                PendingModification.objects.filter(target_object_class=model.__name__).delete()
                for pending_modification_dict in objects:
                    pending_modification = PendingModification(**pending_modification_dict)
                    pending_modification.apply_modification()
                    
                    synced_objects.append(pending_modification.target_object().pk)
                    
                model.objects.exclude(pk__in=synced_objects).delete()
