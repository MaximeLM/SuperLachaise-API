# -*- coding: utf-8 -*-

"""
sync_wikimedia_commons_categories.py
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

import json, os, re, requests, sys, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def print_unicode(str):
    print str.encode('utf-8')

class Command(BaseCommand):
    
    def request_wikimedia_commons_categories(self, wikimedia_commons_categories):
        pages = {}
        
        last_continue = {
            'continue': '',
        }
        
        categories = '|'.join(wikimedia_commons_categories).encode('utf8')
        
        while True:
            # Request properties
            params = {
                'action': 'query',
                'prop': 'title|revisions',
                'rvprop': 'content',
                'format': 'json',
                'titles': categories,
            }
            params.update(last_continue)
            
            if settings.MEDIAWIKI_USER_AGENT:
                headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
            
            if 'pages' in json_result['query']:
                pages.update(json_result['query']['pages'])
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return pages
    
    def request_image_list(self, wikimedia_commons_category):
        category_members = []
        pages = {}
        
        last_continue = {
            'continue': '',
        }
        
        category = 'Category:%s' % wikimedia_commons_category.encode('utf8')
        
        while True:
            # Request properties
            params = {
                'action': 'query',
                'prop': 'revisions',
                'list': 'categorymembers',
                'cmtype': 'file',
                'rvprop': 'content',
                'format': 'json',
                'cmtitle': category,
                'titles': category,
            }
            params.update(last_continue)
            
            if settings.MEDIAWIKI_USER_AGENT:
                headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
            
            if 'categorymembers' in json_result['query']:
                category_members.extend(json_result['query']['categorymembers'])
            if 'pages' in json_result['query']:
                pages.update(json_result['query']['pages'])
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return (category_members, pages)
    
    def get_files(self, category_members):
        result = []
        for category_member in category_members:
            result.append(category_member['title']) 
        
        return result
    
    def get_main_image(self, page):
        try:
            if len(page['revisions']) != 1:
                raise BaseException
            wikitext = page['revisions'][0]['*']
            
            main_image = u''
            for line in wikitext.split('\n'):
                match_obj = re.search(r'^.*[iI]mage.*\=[\s]*(.*)[\s]*$', line)
                if match_obj:
                    main_image = match_obj.group(1).strip()
                    break
            
            if main_image:
                main_image = u'File:' + main_image
            
            return main_image
        except:
            return u''
    
    def handle_wikimedia_commons_category(self, page):
        target_object_id_dict = {"wikimedia_commons_id": page['title']}
        
        # Get values
        values_dict = {
            'main_image': self.get_main_image(page),
            'deleted': False,
        }
        
        # Get element in database if it exists
        wikimedia_commons_category = WikimediaCommonsCategory.objects.filter(**target_object_id_dict).first()
        
        if not wikimedia_commons_category:
            # Creation
            pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=json.dumps(target_object_id_dict))
            self.fetched_pending_modifications_pks.append(pending_modification.pk)
            pending_modification.action = PendingModification.CREATE_OR_UPDATE
            
            self.created_objects = self.created_objects + 1
            pending_modification.modified_fields = json.dumps(values_dict)
            pending_modification.full_clean()
            pending_modification.save()
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            self.fetched_objects_pks.append(wikimedia_commons_category.pk)
            
            modified_fields = {}
            for field, value in values_dict.iteritems():
                if value != getattr(wikimedia_commons_category, field):
                    modified_fields[field] = value
            
            if modified_fields:
                # Modification
                pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=json.dumps(target_object_id_dict))
                self.fetched_pending_modifications_pks.append(pending_modification.pk)
                pending_modification.action = PendingModification.CREATE_OR_UPDATE
                
                self.modified_objects = self.modified_objects + 1
                pending_modification.modified_fields = json.dumps(modified_fields)
                pending_modification.full_clean()
                pending_modification.save()
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete previous modification if any
                pending_modification = PendingModification.objects.filter(target_object_class="WikimediaCommonsCategory", target_object_id=json.dumps(target_object_id_dict)).delete()
    
    def sync_wikimedia_commons_categories(self, param_wikimedia_commons_categories):
        # Get wikimedia commons categories
        wikimedia_commons_categories = []
        if param_wikimedia_commons_categories:
            wikimedia_commons_categories = param_wikimedia_commons_categories.split('|')
        else:
            for openstreetmap_element in OpenStreetMapElement.objects.filter(wikimedia_commons__startswith='Category:'):
                link = openstreetmap_element.wikimedia_commons
                if not link in wikimedia_commons_categories:
                    wikimedia_commons_categories.append(link)
            for wikidata_entry in WikidataEntry.objects.exclude(wikimedia_commons_category__exact=''):
                sync_category = False
                for instance_of in wikidata_entry.instance_of.split(';'):
                    if instance_of in self.synced_instance_of:
                        sync_category = True
                        break
                if sync_category:
                    link = 'Category:' + wikidata_entry.wikimedia_commons_category
                    if not link in wikimedia_commons_categories:
                        wikimedia_commons_categories.append(link)
            for wikidata_entry in WikidataEntry.objects.exclude(wikimedia_commons_grave_category=''):
                link = 'Category:' + wikidata_entry.wikimedia_commons_grave_category
                if not link in wikimedia_commons_categories:
                    wikimedia_commons_categories.append(link)
        
        print_unicode(_('Requesting Wikimedia Commons...'))
        wikimedia_commons_categories = list(set(wikimedia_commons_categories))
        total = len(wikimedia_commons_categories)
        count = 0
        max_count_per_request = 25
        self.fetched_objects_pks = []
        self.fetched_pending_modifications_pks = []
        for chunk in [wikimedia_commons_categories[i:i+max_count_per_request] for i in range(0,len(wikimedia_commons_categories),max_count_per_request)]:
            print_unicode(str(count) + u'/' + str(total))
            count += len(chunk)
            
            pages = self.request_wikimedia_commons_categories(chunk)
            for page in pages.values():
                self.handle_wikimedia_commons_category(page)
        print_unicode(str(count) + u'/' + str(total))
        
        if not param_wikimedia_commons_categories:
            # Delete pending creations if element was not downloaded
            PendingModification.objects.filter(target_object_class="WikimediaCommonsCategory", action=PendingModification.CREATE_OR_UPDATE).exclude(pk__in=self.fetched_pending_modifications_pks).delete()
        
            # Look for deleted elements
            for wikimedia_commons_category in WikimediaCommonsCategory.objects.exclude(pk__in=self.fetched_objects_pks):
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=json.dumps({"wikimedia_commons_id": wikimedia_commons_category.wikimedia_commons_id}))
            
                pendingModification.action = PendingModification.CREATE_OR_UPDATE
                pendingModification.modified_fields = json.dumps({"deleted": True})
            
                pendingModification.full_clean()
                pendingModification.save()
                self.deleted_objects = self.deleted_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--wikimedia_commons_categories',
            action='store',
            dest='wikimedia_commons_categories')
    
    def handle(self, *args, **options):
        
        try:
            self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0].split('sync_')[-1])
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.auto_apply = (Setting.objects.get(key=u'wikimedia_commons:auto_apply_modifications').value == 'true')
            self.synced_instance_of = json.loads(Setting.objects.get(key=u'wikimedia_commons:synced_instance_of').value)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            self.sync_wikimedia_commons_categories(options['wikimedia_commons_categories'])
            print_unicode(_('== End %s ==') % self.synchronization.name)
            
            self.synchronization.created_objects = self.created_objects
            self.synchronization.modified_objects = self.modified_objects
            self.synchronization.deleted_objects = self.deleted_objects
            self.synchronization.errors = ', '.join(self.errors)
            
            translation.deactivate()
        except:
            print_unicode(traceback.format_exc())
            error = sys.exc_info()[1]
            self.synchronization.errors = traceback.format_exc()
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        if error:
            raise CommandError(error)
