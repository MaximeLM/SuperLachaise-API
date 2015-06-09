# -*- coding: utf-8 -*-

"""
sync_wikipedia.py
superlachaise_api

Created by Maxime Le Moine on 09/06/2015.
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

import json, os, requests, sys, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from HTMLParser import HTMLParser

from superlachaise_api.models import *

class WikipediaIntroHTMLParser(HTMLParser):
    
    def __init__(self, language_code):
        self.reset()
        
        self.language_code = language_code
        self.result = []
        self.opened_tags = [{'tag': 'root', 'attrs': [], 'data': False, 'content': self.result}]
        self.current_content = self.result
        self.data = False
    
    def can_read_data(self):
        if len(self.opened_tags) > 1 and self.opened_tags[1]['tag'] == 'div':
            return False
        
        for opened_tag in self.opened_tags:
            if opened_tag['tag'] == 'table':
                return False
            if opened_tag['tag'] == 'ref':
                return False
            if opened_tag['tag'] == 'ol':
                for attr in opened_tag['attrs']:
                    if attr[0] in ['id', 'class']:
                        return False
            if opened_tag['tag'] == 'ul':
                for attr in opened_tag['attrs']:
                    if attr[0] in ['id', 'class']:
                        return False
            if opened_tag['tag'] == 'strong':
                for attr in opened_tag['attrs']:
                    if attr[0] == 'class' and 'error' in attr[1]:
                        return False
            if opened_tag['tag'] == 'sup':
                for attr in opened_tag['attrs']:
                    if attr[0] in ['id', 'class']:
                        return False
            if opened_tag['tag'] == 'span':
                for attr in opened_tag['attrs']:
                    if attr[0] == 'id' or (attr[0] == 'class' and attr[1] in ['noprint', 'unicode haudio']):
                        return False
            if opened_tag['tag'] == 'small':
                for attr in opened_tag['attrs']:
                    if attr[0] == 'id' or (attr[0] == 'class' and 'metadata' in attr[1]):
                        return False
            if opened_tag['tag'] == 'li':
                for attr in opened_tag['attrs']:
                    if attr[0] in ['id', 'class']:
                        return False
        
        return True
    
    def handle_data(self, data):
        if self.can_read_data():
            self.current_content.append(data)
            self.opened_tags[-1]['data'] = True
    
    def handle_entityref(self, name):
        if self.can_read_data():
            self.current_content.append('&'+name+';')
            self.opened_tags[-1]['data'] = True
    
    def handle_charref(self, name):
        if self.can_read_data():
            self.current_content.append('&#'+name+';')
            self.opened_tags[-1]['data'] = True
    
    def handle_starttag(self, tag, attrs):
        self.current_content = []
        self.opened_tags.append({'tag': tag, 'attrs': attrs, 'data': False, 'content': self.current_content})
        
        if self.can_read_data():
            self.current_content.append('<%s' % tag)
            
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        if attr[1].startswith('/wiki/') or attr[1].startswith('/w/'):
                            self.current_content.append(' href="https://{language_code}.wikipedia.org{link}"'.format(language_code=self.language_code, link=attr[1]))
                        elif attr[1].startswith('//'):
                            self.current_content.append(' href="http:{link}"'.format(link=attr[1]))
            
            self.current_content.append('>')
    
    def handle_endtag(self, tag):
        if self.can_read_data():
            self.current_content.append('</%s>' % tag)
        
        if self.can_read_data() and (self.opened_tags[-1]['data'] or self.opened_tags[-1]['tag'] == 'a'):
            self.opened_tags[-2]['content'].append(''.join(self.current_content))
            self.opened_tags[-2]['data'] = True
        else:
            # Delete last whitespace if any
            content = self.opened_tags[-2]['content']
            while isinstance(content, list):
                if len(content) > 0:
                    if not isinstance(content[-1], list) and content[-1] in [u' ', u'&nbsp;']:
                        del content[-1]
                        if len(content) < 2:
                            self.opened_tags[-2]['data'] = False
                        break
                    content = content[-1]
                else:
                    content = None
        self.opened_tags = self.opened_tags[:-1]
        self.current_content = self.opened_tags[-1]['content']
    
    def get_data(self):
        return ''.join(self.result).strip()

class Command(BaseCommand):
    
    def request_wikipedia_pre_section(self, language_code, title):
        # Request properties
        params = {
            'action': 'parse',
            'prop': 'text',
            'section': '0',
            'format': 'json',
            'page': title.encode('utf8'),
        }
        
        if settings.USER_AGENT:
            headers = {"User-Agent" : settings.USER_AGENT}
        else:
            raise 'no USER_AGENT defined in settings.py'
        
        json_result = requests.get('https://%s.wikipedia.org/w/api.php' % (language_code), params=params, headers=headers).json()
        
        return json_result['parse']['text']['*']
    
    def get_wikipedia_intro(self, language_code, title):
        # Get wikipedia pre-section (intro)
        pre_section = self.request_wikipedia_pre_section(language_code, title)
        
        # Process HTML
        parser = WikipediaIntroHTMLParser(language_code)
        parser.feed(pre_section)
        
        return parser.get_data()
    
    def hande_wikidata_localized_entry(self, wikidata_localized_entry):
        id = wikidata_localized_entry.language.code + u':' + wikidata_localized_entry.wikidata_entry_id
        values_dict = {
            'intro': self.get_wikipedia_intro(wikidata_localized_entry.language.code, wikidata_localized_entry.wikipedia),
        }
        
        # Get element in database if it exists
        wikipedia_page = WikipediaPage.objects.filter(id=id).first()
        
        if not wikipedia_page:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
            
            pendingModification.action = PendingModification.CREATE
            pendingModification.modified_fields = json.dumps(values_dict)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            # Search for modifications
            modified_values = {}
            
            for field, value in values_dict.iteritems():
                if value != getattr(wikipedia_page, field):
                    modified_values[field] = value
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = PendingModification.MODIFY
            
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                PendingModification.objects.filter(target_object_class="WikipediaPage", target_object_id=id).delete()
    
    def sync_wikipedia(self, wikidata_localized_entry_ids):
        if wikidata_localized_entry_ids:
            wikidata_localized_entries = WikidataLocalizedEntry.objects.filter(id__in=wikidata_localized_entry_ids.split('|')).exclude(wikipedia__exact='')
        else:
            wikidata_localized_entries = WikidataLocalizedEntry.objects.exclude(wikipedia__exact='')
        total = len(wikidata_localized_entries)
        count = 0
        fetched_ids = []
        for wikidata_localized_entry in wikidata_localized_entries:
            print str(count) + u'/' + str(total)
            count += 1
            fetched_ids.append(wikidata_localized_entry.language.code + u':' + wikidata_localized_entry.wikidata_entry_id)
            self.hande_wikidata_localized_entry(wikidata_localized_entry)
        print str(count) + u'/' + str(total)
        
        if not wikidata_localized_entry_ids:
            # Delete pending creations if element was not fetched
            PendingModification.objects.filter(target_object_class="WikipediaPage", action=PendingModification.CREATE).exclude(target_object_id__in=fetched_ids).delete()
        
            # Look for deleted elements
            for wikipedia_page in WikipediaPage.objects.exclude(id__in=fetched_ids):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=str(wikipedia_page.wikidata_localized_entry_id))
                
                pendingModification.action = PendingModification.DELETE
                pendingModification.modified_fields = u''
            
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--wikidata_localized_entry_ids',
            action='store',
            dest='wikidata_localized_entry_ids')
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(key=u'wikipedia:auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_wikipedia(options['wikidata_localized_entry_ids'])
            
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
