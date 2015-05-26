# -*- coding: utf-8 -*-

"""
load_initial_data.py
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

from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
import os

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../../initial_data/settings.json') as data_file:    
            for obj in serializers.deserialize("json", data_file):
                obj.save()
        
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../../initial_data/admin_commands.json') as data_file:    
            for obj in serializers.deserialize("json", data_file):
                obj.save()
