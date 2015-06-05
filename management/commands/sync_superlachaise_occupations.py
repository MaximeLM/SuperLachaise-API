# -*- coding: utf-8 -*-

"""
sync_wikidata.py
superlachaise_api

Created by Maxime Le Moine on 28/05/2015.
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

import datetime, json, os, sys, time, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def sync_superlachaise_occupations(self):
        for wikidata_entry in WikidataEntry.objects.all():
            if wikidata_entry.occupations:
                for occupation in wikidata_entry.occupations.split(';'):
                    superlachaise_occupation, created = SuperLachaiseOccupation.objects.get_or_create(id=occupation)
                    if created:
                        self.created_objects += 1
                    superlachaise_occupation.save()
                    if not superlachaise_occupation in wikidata_entry.superlachaise_occupations.all():
                        wikidata_entry.superlachaise_occupations.add(superlachaise_occupation.id)
                for superlachaise_occupation in wikidata_entry.superlachaise_occupations.all():
                    if not superlachaise_occupation.id in wikidata_entry.occupations.split(';'):
                        wikidata_entry.superlachaise_occupations.remove(superlachaise_occupation.id)
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.created_objects = 0
            
            self.sync_superlachaise_occupations()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            
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
