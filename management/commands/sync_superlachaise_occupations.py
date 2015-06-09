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

import datetime, json, os, requests, sys, time, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def request_wikidata(self, wikidata_codes):
        result = {}
        last_continue = {
            'continue': '',
        }
        languages = Language.objects.all().values_list('code', flat=True)
        ids = '|'.join(wikidata_codes).encode('utf8')
        
        while True:
            # Request properties
            params = {
                'languages': languages,
                'action': 'wbgetentities',
                'props': 'labels',
                'format': 'json',
                'ids': ids,
            }
            params.update(last_continue)
            
            if settings.USER_AGENT:
                headers = {"User-Agent" : settings.USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://www.wikidata.org/w/api.php', params=params, headers=headers).json()
            
            if 'entities' in json_result:
                result.update(json_result['entities'])
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return result
    
    def sync_superlachaise_occupations(self):
        # Sync objects
        for wikidata_entry in WikidataEntry.objects.exclude(occupations__exact=''):
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
        
        # Sync names from Wikidata
        wikidata_codes = SuperLachaiseOccupation.objects.all().values_list('id', flat=True)
        
        print 'Requesting Wikidata...'
        wikidata_entities = {}
        total = len(wikidata_codes)
        count = 0
        max_count_per_request = 25
        wikidata_codes = list(set(wikidata_codes))
        for chunk in [wikidata_codes[i:i+max_count_per_request] for i in range(0,len(wikidata_codes),max_count_per_request)]:
            print str(count) + u'/' + str(total)
            count += len(chunk)
            
            wikidata_entities.update(self.request_wikidata(chunk))
        print str(count) + u'/' + str(total)
        
        for superlachaise_occupation in SuperLachaiseOccupation.objects.all():
            wikidata_entity = wikidata_entities[superlachaise_occupation.id]
            names = {}
            for language in Language.objects.all():
                try:
                    name = wikidata_entity['labels'][language.code]['value']
                    if not name in names:
                        names[name] = []
                    names[name].append(language.code)
                except:
                    pass
            
            if len(names) > 0:
                result = []
                for name, languages in names.iteritems():
                    result.append('(%s)%s' % (','.join(languages), name))
                superlachaise_occupation.name = '; '.join(result)
            else:
                superlachaise_occupation.name = u''
            superlachaise_occupation.save()
    
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
