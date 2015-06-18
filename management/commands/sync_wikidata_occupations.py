# -*- coding: utf-8 -*-

"""
sync_wikidata_occupations.py
superlachaise_api

Created by Maxime Le Moine on 11/06/2015.
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

def print_unicode(str):
    print str.encode('utf-8')

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
            
            if settings.MEDIAWIKI_USER_AGENT:
                headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://www.wikidata.org/w/api.php', params=params, headers=headers).json()
            
            if 'entities' in json_result:
                result.update(json_result['entities'])
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return result
    
    def sync_wikidata_occupations(self):
        # Sync objects
        for wikidata_entry in WikidataEntry.objects.exclude(occupations__exact=''):
            for occupation in wikidata_entry.occupations.split(';'):
                wikidata_occupation, created = WikidataOccupation.objects.get_or_create(id=occupation)
                if created:
                    self.created_objects += 1
                wikidata_occupation.save()
                if not wikidata_occupation in wikidata_entry.wikidata_occupations.all():
                    wikidata_entry.wikidata_occupations.add(wikidata_occupation.id)
            for wikidata_occupation in wikidata_entry.wikidata_occupations.all():
                if not wikidata_occupation.id in wikidata_entry.occupations.split(';'):
                    wikidata_entry.wikidata_occupations.remove(wikidata_occupation.id)
        
        # Sync names from Wikidata
        wikidata_codes = WikidataOccupation.objects.all().values_list('id', flat=True)
        
        print_unicode(_('Requesting Wikidata...'))
        wikidata_entities = {}
        total = len(wikidata_codes)
        count = 0
        max_count_per_request = 25
        wikidata_codes = list(set(wikidata_codes))
        for chunk in [wikidata_codes[i:i+max_count_per_request] for i in range(0,len(wikidata_codes),max_count_per_request)]:
            print_unicode(str(count) + u'/' + str(total))
            count += len(chunk)
            
            wikidata_entities.update(self.request_wikidata(chunk))
        print_unicode(str(count) + u'/' + str(total))
        
        for wikidata_occupation in WikidataOccupation.objects.all():
            wikidata_entity = wikidata_entities[wikidata_occupation.id]
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
                wikidata_occupation.name = '; '.join(result)
            else:
                wikidata_occupation.name = u''
            wikidata_occupation.save()
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0])
        error_message = None
        
        try:
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            
            self.created_objects = 0
            
            self.sync_wikidata_occupations()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            
            if result_list:
                self.synchronization.last_result = ', '.join(result_list)
            else:
                self.synchronization.last_result = Synchronization.NO_MODIFICATIONS
        except:
            traceback.print_exc()
            exception = sys.exc_info()[0]
            error_message = exception.__class__.__name__ + ': ' + traceback.format_exc()
            self.synchronization.last_result = error_message
        
        print_unicode(_('== End %s ==') % self.synchronization.name)
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        translation.deactivate()
        
        return error_message
