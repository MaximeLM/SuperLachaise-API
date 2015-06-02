# -*- coding: utf-8 -*-

"""
sync_wikipedia.py
superlachaise_api

Created by Maxime Le Moine on 31/05/2015.
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
                    if attr[0] == 'id' or (attr[0] == 'class' and attr[1] == 'noprint'):
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
                            self.current_content.append(' href="http://{language_code}.wikipedia.org{link}"'.format(language_code=self.language_code, link=attr[1]))
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
    
    def request_wikipedia_pre_section(self, language, title):
        # Request properties
        url = "http://{language_code}.wikipedia.org/w/api.php?action=parse&page={title}&format=json&prop=text&section=0"\
            .format(language_code=language.code, title=urllib2.quote(title.encode('utf8')))
        request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
        u = urllib2.urlopen(request)
        
        # Parse result
        data = u.read()
        json_result = json.loads(data)
        
        return json_result['parse']['text']['*']
    
    def get_wikipedia_intro(self, language, title):
        # Get wikipedia pre-section (intro)
        pre_section = self.request_wikipedia_pre_section(language, title)
        
        # Process HTML
        parser = WikipediaIntroHTMLParser(language.code)
        parser.feed(pre_section)
        
        return parser.get_data()
    
    def handle_wikipedia_info(self, language, wikipedia_info, count):
        title = wikipedia_info['title']
        id = language.code + ':' + title
        self.fetched_ids.append(id)
        
        print str(count) + u'-' + id
        
        values_dict = {
            'intro': self.get_wikipedia_intro(language, title),
        }
        
        # Get element in database if it exists
        wikipedia_page = WikipediaPage.objects.filter(language=language, title=title).first()
        request_page_download = False
        modified_fields = {}
        
        if not wikipedia_page:
            # Creation
            pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
            pending_modification.action = PendingModification.CREATE
            
            self.created_objects = self.created_objects + 1
            pending_modification.modified_fields = json.dumps(values_dict)
            pending_modification.full_clean()
            pending_modification.save()
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            modified_fields = {}
            for field, value in values_dict.iteritems():
                if value != getattr(wikipedia_page, field):
                    modified_fields[field] = value
            
            if modified_fields:
                # Modification
                pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=id)
                pending_modification.action = PendingModification.MODIFY
                
                self.modified_objects = self.modified_objects + 1
                pending_modification.modified_fields = json.dumps(modified_fields)
                pending_modification.full_clean()
                pending_modification.save()
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete previous modification if any
                pending_modification = PendingModification.objects.filter(target_object_class="WikipediaPage", target_object_id=id).first()
                if pending_modification:
                    pending_modification.delete()
    
    def sync_wikipedia(self):
        # Get wikipedia links on localized Wikidata entries
        wikipedia_links = {}
        if self.wikipedia_ids:
            for wikipedia_id in self.wikipedia_ids.split('|'):
                language = Language.objects.get(code=wikipedia_id.split(':')[0])
                link = wikipedia_id.split(':')[1]
                if link:
                    if not language in wikipedia_links:
                        wikipedia_links[language] = []
                    if not link in wikipedia_links[language]:
                        wikipedia_links[language].append(link)
        else:
            for wikidata_localized_entry in WikidataLocalizedEntry.objects.all():
                language = wikidata_localized_entry.language
                link = wikidata_localized_entry.wikipedia
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
            count = len(wikipedia_infos[language])
            for wikipedia_info in wikipedia_infos[language].values():
                self.handle_wikipedia_info(language, wikipedia_info, count)
                count = count - 1
        
        if not self.wikipedia_ids:
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
    
    def add_arguments(self, parser):
        parser.add_argument('--wikipedia_ids',
            action='store',
            dest='wikipedia_ids')
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        self.admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.auto_apply = (Setting.objects.get(category='Wikipedia', key=u'auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = 0
            self.fetched_ids = []
            self.wikipedia_ids = options['wikipedia_ids']
            
            self.sync_wikipedia()
            
            result_list = []
            if self.created_objects > 0:
                result_list.append(_('{nb} object(s) created').format(nb=self.created_objects))
            if self.modified_objects > 0:
                result_list.append(_('{nb} object(s) modified').format(nb=self.modified_objects))
            if self.deleted_objects > 0:
                result_list.append(_('{nb} object(s) deleted').format(nb=self.deleted_objects))
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
