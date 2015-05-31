# -*- coding: utf-8 -*-

"""
sync_OpenStreetMap.py
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

import json, os ,sys, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def request_wikipedia_infos(self, wikipedia_links):
        max_items_per_request = 25
        
        result = {}
        for language, links in wikipedia_links.iteritems():
            i = 0
            result_for_language = {}
            while i < len(links):
                links_page = links[i : min(len(links), i + max_items_per_request)]
                
                # Request properties
                url = "http://{language_code}.wikipedia.org/w/api.php?action=query&prop=info&format=json&titles={titles}"\
                    .format(language_code=language.code, titles=urllib2.quote('|'.join(links_page).encode('utf8'), '|'))
                request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
                u = urllib2.urlopen(request)
                
                # Parse result
                data = u.read()
                json_result = json.loads(data)
                
                result_for_language.update(json_result['query']['pages'])
                
                i = i + max_items_per_request
            result[language] = result_for_language
        
        return result
    
    def handle_wikipedia_info(self, language, wikipedia_info):
        title = wikipedia_info['title']
        last_revision_id = wikipedia_info['lastrevid']
        id = language.code + ':' + title
        self.fetched_ids.append(id)
        
        # Get element in database if it exists
        wikipedia_page = WikipediaPage.objects.filter(language=language, title=title).first()
        request_page_download = False
        
        if not wikipedia_page:
            # Creation
            pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
            pending_modification.action = PendingModification.CREATE
            modified_fields = json.loads(pending_modification.modified_fields) if pending_modification.modified_fields else {}
            modified_fields = {'last_revision_id': last_revision_id, 'intro': u''}
            request_page_download = True
            self.created_objects = self.created_objects + 1
        else:
            if not wikipedia_page.last_revision_id == last_revision_id:
                # Modification
                pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
                pending_modification.action = PendingModification.MODIFY
                modified_fields = json.loads(pending_modification.modified_fields) if pending_modification.modified_fields else {}
                modified_fields = {'last_revision_id': last_revision_id, 'intro': u''}
                request_page_download = True
                self.modified_objects = self.modified_objects + 1
            else:
                # Delete previous modification if any
                pending_modification = PendingModification.objects.filter(target_object_class="WikipediaPage", target_object_id=id).first()
                if pending_modification:
                    modified_fields = json.loads(pending_modification.modified_fields) if pending_modification.modified_fields else {}
                    modified_fields.pop('last_revision_id', None)
                    if not modified_fields:
                        pending_modification.delete()
        
        if request_page_download:
            pending_modification.modified_fields = json.dumps(modified_fields)
            pending_modification.full_clean()
            pending_modification.save()
            
            if self.auto_apply:
                pendingModification.apply_modification()
    
    def sync_wikipedia(self):
        # Get wikipedia links on localized Wikidata entries
        wikipedia_links = {}
        for localized_wikidata_entry in LocalizedWikidataEntry.objects.all():
            language = localized_wikidata_entry.language
            link = localized_wikidata_entry.wikipedia
            if link:
                if not language in wikipedia_links:
                    wikipedia_links[language] = []
                if not link in wikipedia_links[language]:
                    wikipedia_links[language].append(link)
        
        # Download page properties
        if wikipedia_links:
            wikipedia_infos = self.request_wikipedia_infos(wikipedia_links)
        
        # Handle results
        for language in wikipedia_infos:
            for wikipedia_info in wikipedia_infos[language].values():
                self.handle_wikipedia_info(language, wikipedia_info)
        
        # Delete pending creations if element was not downloaded
        for pendingModification in PendingModification.objects.filter(target_object_class="WikipediaPage", action=PendingModification.CREATE):
            if not pendingModification.target_object_id in self.fetched_ids:
                pendingModification.delete()
    
        # Look for deleted elements
        for wikipedia_page in WikipediaPage.objects.all():
            id = wikipedia_page.language.code + u':' + wikipedia_page.title
            if not id in self.fetched_ids:
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
            
                pendingModification.action = PendingModification.DELETE
                pendingModification.modified_fields = u''
            
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(category='Wikipedia', key=u'auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.fetched_ids = []
            
            self.sync_wikipedia()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.deleted_objects > 0:
                result_list.append(_('{nb} object(s) deleted').format(nb=self.deleted_objects))
            
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
