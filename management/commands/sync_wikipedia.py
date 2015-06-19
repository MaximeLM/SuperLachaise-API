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

import json, os, re, requests, sys, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from HTMLParser import HTMLParser

from superlachaise_api.models import *

def print_unicode(str):
    print str.encode('utf-8')

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
    
    def request_wikipedia_pages(self, language_code, wikipedia_titles):
        pages = {}
        
        last_continue = {
            'continue': '',
        }
        
        titles = '|'.join(wikipedia_titles).encode('utf8')
        
        while True:
            # Request properties
            params = {
                'action': 'query',
                'prop': 'revisions',
                'rvprop': 'content',
                'format': 'json',
                'titles': titles,
            }
            params.update(last_continue)
            
            if settings.MEDIAWIKI_USER_AGENT:
                headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://%s.wikipedia.org/w/api.php' % (language_code), params=params, headers=headers).json()
            
            if 'pages' in json_result['query']:
                for page in json_result['query']['pages'].values():
                    pages[page['title']] = page
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return pages
    
    def request_wikipedia_pre_section(self, language_code, title):
        # Request properties
        params = {
            'action': 'parse',
            'prop': 'text',
            'section': '0',
            'format': 'json',
            'page': title.encode('utf8'),
        }
        
        if settings.MEDIAWIKI_USER_AGENT:
            headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
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
    
    def get_default_sort(self, page):
        try:
            if len(page['revisions']) != 1:
                raise BaseException
            wikitext = page['revisions'][0]['*']
            
            default_sort = u''
            for line in wikitext.split('\n'):
                match_obj = re.search(r'^{{DEFAULTSORT:(.*)}}$', line)
                if match_obj:
                    default_sort = match_obj.group(1).strip()
                    break
                match_obj = re.search(r'^{{CLEDETRI:(.*)}}$', line)
                if match_obj:
                    default_sort = match_obj.group(1).strip()
                    break
            
            return default_sort
        except:
            return u''
    
    def hande_wikidata_localized_entry(self, wikidata_localized_entry):
        target_object_id_dict = {"wikidata_localized_entry_id": wikidata_localized_entry.pk}
        
        values_dict = {
            'intro': self.get_wikipedia_intro(wikidata_localized_entry.language.code, wikidata_localized_entry.wikipedia),
        }
        
        if wikidata_localized_entry.language.code in self.default_sort and wikidata_localized_entry.wikipedia in self.default_sort[wikidata_localized_entry.language.code]:
            values_dict['default_sort'] = self.default_sort[wikidata_localized_entry.language.code][wikidata_localized_entry.wikipedia]
        else:
            values_dict['default_sort'] = u''
        
        # Get element in database if it exists
        wikipedia_page = WikipediaPage.objects.filter(**target_object_id_dict).first()
        
        if not wikipedia_page:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pendingModification.pk)
            
            pendingModification.action = PendingModification.CREATE_OR_UPDATE
            pendingModification.modified_fields = json.dumps(values_dict)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.fetched_objects_pks.append(wikipedia_page.pk)
            
            # Search for modifications
            modified_values = {}
            
            for field, value in values_dict.iteritems():
                if value != getattr(wikipedia_page, field):
                    modified_values[field] = value
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=json.dumps(target_object_id_dict))
                self.fetched_pending_modifications_pks.append(pendingModification.pk)
                pendingModification.modified_fields = json.dumps(modified_values)
                pendingModification.action = PendingModification.CREATE_OR_UPDATE
            
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                PendingModification.objects.filter(target_object_class="WikipediaPage", target_object_id=json.dumps(target_object_id_dict)).delete()
    
    def sync_wikipedia(self, wikidata_localized_entry_ids):
        if wikidata_localized_entry_ids:
            wikidata_localized_entries = WikidataLocalizedEntry.objects.filter(id__in=wikidata_localized_entry_ids.split('|')).exclude(wikipedia__exact='')
        else:
            wikidata_localized_entries = WikidataLocalizedEntry.objects.exclude(wikipedia__exact='')
        
        print_unicode(_('Requesting Wikipedia revisions...'))
        self.default_sort = {}
        total = len(wikidata_localized_entries)
        count = 0
        max_count_per_request = 25
        for language in Language.objects.all():
            self.default_sort[language.code] = {}
            wikipedia_titles = wikidata_localized_entries.filter(language=language).values_list('wikipedia', flat=True)
            for chunk in [wikipedia_titles[i:i+max_count_per_request] for i in range(0,len(wikipedia_titles),max_count_per_request)]:
                print_unicode(str(count) + u'/' + str(total))
                count += len(chunk)
            
                pages_result = self.request_wikipedia_pages(language.code, chunk)
                for title, page in pages_result.iteritems():
                    self.default_sort[language.code][title] = self.get_default_sort(page)
        print_unicode(str(count) + u'/' + str(total))
        
        print_unicode(_('Requesting Wikipedia page content...'))
        total = len(wikidata_localized_entries)
        count = 0
        max_count_per_request = 25
        self.fetched_objects_pks = []
        self.fetched_pending_modifications_pks = []
        for chunk in [wikidata_localized_entries[i:i+max_count_per_request] for i in range(0,len(wikidata_localized_entries),max_count_per_request)]:
            print_unicode(str(count) + u'/' + str(total))
            count += len(chunk)
            
            for wikidata_localized_entry in chunk:
                self.hande_wikidata_localized_entry(wikidata_localized_entry)
        print_unicode(str(count) + u'/' + str(total))
        
        if not wikidata_localized_entry_ids:
            # Delete pending creations if element was not fetched
            PendingModification.objects.filter(target_object_class="WikipediaPage", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
        
            # Look for deleted elements
            for wikipedia_page in WikipediaPage.objects.exclude(pk__in=self.fetched_objects_pks):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikipediaPage", target_object_id=json.dumps({"wikidata_localized_entry_id": wikipedia_page.wikidata_localized_entry.pk}))
                
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
        
        try:
            self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0].split('sync_')[-1])
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.auto_apply = (Setting.objects.get(key=u'wikipedia:auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            self.sync_wikipedia(options['wikidata_localized_entry_ids'])
            print_unicode(_('== End %s ==') % self.synchronization.name)
            
            self.synchronization.created_objects = self.created_objects
            self.synchronization.modified_objects = self.modified_objects
            self.synchronization.deleted_objects = self.deleted_objects
            self.synchronization.errors = ', '.join(self.errors)
            
            translation.deactivate()
        except:
            print_unicode(traceback.format_exc())
            error = sys.exc_info()[1]
            self.synchronization.errors = error
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        if error:
            raise CommandError(error)
