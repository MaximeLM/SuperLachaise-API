# -*- coding: utf-8 -*-

"""
sync_openstreetmap.py
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

import json, sys, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def request_wikidata_with_wikipedia_links(self, language_code, wikipedia_links):
        # List languages to request
        languages = []
        for language in Language.objects.all():
            languages.append(language.code)
        
        # List props to request
        props = ['sitelinks']
        
        max_items_per_request = 25
        
        result = {}
        
        i = 0
        while i < len(wikipedia_links):
            wikipedia_links_page = wikipedia_links[i : min(len(wikipedia_links), i + max_items_per_request)]
        
            # Request properties
            url = u"http://www.wikidata.org/w/api.php?languages={languages}&action=wbgetentities&sites={sites}&titles={titles}&props={props}&format=json"\
                .format(languages='|'.join(languages), titles=urllib2.quote('|'.join(wikipedia_links_page).encode('utf8'), '|'), props='|'.join(props), sites=language_code + 'wiki')
            request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
            u = urllib2.urlopen(request)
        
            # Parse result
            data = u.read()
            json_result = json.loads(data)
            
            # Add entities to result
            result.update(json_result['entities'])
        
            i = i + max_items_per_request
        
        return result
    
    def get_wikipedia(self, entity, language_code):
        try:
            wikipedia = entity['sitelinks'][language_code + 'wiki']
            
            return wikipedia['title']
        except:
            return None
    
    def make_wikidata_combined(self):
        wikipedia_links = {}
        for openstreetmap_element in OpenStreetMapElement.objects.all():
            for wikipedia in openstreetmap_element.wikipedia.split(';'):
                if ':' in wikipedia:
                    language_code = wikipedia.split(':')[-2]
                    link = wikipedia.split(':')[-1]
                    if not language_code in wikipedia_links:
                        wikipedia_links[language_code] = []
                    if not link in wikipedia_links[language_code]:
                        wikipedia_links[language_code].append(link)
        
        entities = {}
        if wikipedia_links:
            for language_code, links in wikipedia_links.iteritems():
                entities.update(self.request_wikidata_with_wikipedia_links(language_code, links))
        
        wikidata_codes_for_openstreetmap_elements = {}
        for wikidata_code, entity in entities.iteritems():
            for language_code in wikipedia_links:
                wikipedia = self.get_wikipedia(entity, language_code)
                if wikipedia:
                    for openstreetmap_element in OpenStreetMapElement.objects.filter(wikipedia__contains=(language_code + u':' + wikipedia)):
                        if not openstreetmap_element in wikidata_codes_for_openstreetmap_elements:
                            wikidata_codes_for_openstreetmap_elements[openstreetmap_element] = []
                        wikidata_codes_for_openstreetmap_elements[openstreetmap_element].append(wikidata_code)
        
        for openstreetmap_element in OpenStreetMapElement.objects.all():
            wikidata_codes = wikidata_codes_for_openstreetmap_elements[openstreetmap_element] if openstreetmap_element in wikidata_codes_for_openstreetmap_elements else []
            if not len(wikidata_codes) == (len(openstreetmap_element.wikipedia.split(';')) if openstreetmap_element.wikipedia else 0):
                self.errors = self.errors + 1
                admin_command_error = AdminCommandError(admin_command=self.admin_command, type=_('wikipedia page not found'))
                admin_command_error.description = _("A wikipedia page of an OpenStreetMap element could not be found.")
                admin_command_error.target_object_class = "OpenStreetMapElement"
                admin_command_error.target_object_id = openstreetmap_element.id
                
                admin_command_error.full_clean()
                admin_command_error.save()
            else:
                wikidata_combined = openstreetmap_element.wikidata.split(';') if openstreetmap_element.wikidata else []
                for wikidata_code in wikidata_codes:
                    if not wikidata_code in wikidata_combined:
                        wikidata_combined.append(wikidata_code)
                wikidata_combined.sort()
                
                if not ';'.join(wikidata_combined) == openstreetmap_element.wikidata_combined:
                    pendingModification, created = PendingModification.objects.get_or_create(target_object_class="OpenStreetMapElement", target_object_id=str(openstreetmap_element.id))
                    modified_fields = json.loads(pendingModification.modified_fields) if pendingModification.modified_fields else {}
                    modified_fields['wikidata_combined'] = ';'.join(wikidata_combined)
                    
                    if not modified_fields:
                        pendingModification.delete()
                    else:
                        pendingModification.modified_fields = json.dumps(modified_fields)
                        pendingModification.action = "modify"
                        pendingModification.full_clean()
                        pendingModification.save()
                        self.modified_objects = self.modified_objects + 1
                    
                if self.auto_apply:
                    pendingModification.apply_modification()
    
    def handle(self, *args, **options):
        
        translation.activate(settings.LANGUAGE_CODE)
        
        self.admin_command = AdminCommand.objects.get(name='make_wikidata_combined')
        
        self.auto_apply = (Setting.objects.get(category='OpenStreetMap', key=u'auto_apply_modifications').value == 'true')
        
        self.modified_objects = 0
        self.errors = 0
        
        AdminCommandError.objects.filter(admin_command=self.admin_command).delete()
        
        try:
            self.make_wikidata_combined()
            
            result_list = []
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.errors > 0:
                result_list.append(_('{nb} error(s)').format(nb=self.errors))
            
            if result_list:
                self.admin_command.last_result = ', '.join(result_list)
            else:
                self.admin_command.last_result = _("No modifications")
        except:
            exception = sys.exc_info()[0]
            self.admin_command.last_result = exception.__class__.__name__ + ': ' + traceback.format_exc()
        
        self.admin_command.last_executed = timezone.now()
        self.admin_command.save()
        
        translation.deactivate()
