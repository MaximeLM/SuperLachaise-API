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
from superlachaise_api.management.commands.dump_configuration import configuration_models

class Command(BaseCommand):
    
    def resolve_field_relation(self, object_model, field, value):
        """ Convert a field/value pair to object/value if needed e.g. language__code=fr => language=<Language> """
        if '__' in field:
            resolved_field = field.split('__')[0]
            model = object_model._meta.get_field(resolved_field).rel.to
            resolved_value = model.objects.get(**{'__'.join(field.split('__')[1:]): value})
            result = (resolved_field, resolved_value)
        else:
            # Assert field exists
            object_model._meta.get_field(field)
            result = (field, value)
        return result
    
    def handle(self, *args, **options):
        with open(os.path.dirname(__file__) + '/../../configuration/configuration.json', 'r') as configuration_file:
            configuration = json.load(configuration_file)
            
            for model, fields in configuration_models.iteritems():
                for object_fields in configuration[model.__name__]:
                    target_object_id_dict = {}
                    for field in fields['id_fields']:
                        resolved_field, resolved_value = self.resolve_field_relation(model, field, object_fields[field])
                        target_object_id_dict[resolved_field] = resolved_value
                    object, created = model.objects.get_or_create(**target_object_id_dict)
                    for field in fields['other_fields']:
                        setattr(object, field, object_fields[field])
                    object.save()
