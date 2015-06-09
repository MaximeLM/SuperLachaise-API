# -*- coding: utf-8 -*-

"""
sync_wikimedia_commons_files.py
superlachaise_api

Created by Maxime Le Moine on 01/06/2015.
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

import json, os, re, requests, sys, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class Command(BaseCommand):
    
    def request_wikimedia_commons_files(self, wikimedia_commons_files):
        result = {}
        last_continue = {
            'continue': '',
        }
        titles = '|'.join(wikimedia_commons_files).encode('utf8')
        
        while True:
            # Request properties
            params = {
                'action': 'query',
                'prop': 'imageinfo',
                'iiprop': 'url',
                'iiprop': 'url',
                'format': 'json',
                'iiurlwidth': self.thumbnail_width,
                'titles': titles,
            }
            params.update(last_continue)
            
            if settings.USER_AGENT:
                headers = {"User-Agent" : settings.USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
            
            if 'pages' in json_result['query']:
                for page_id, page in json_result['query']['pages'].iteritems():
                    result[page['title']] = page
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return result
    
    def get_original_url(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return image_info[0]['url']
        except:
            return u''
    
    def get_thumbnail_url(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return image_info[0]['thumburl']
        except:
            return u''
    
    def handle_wikimedia_commons_file(self, id, wikimedia_commons_file):
        # Get data
        values_dict = {
            'original_url': self.get_original_url(wikimedia_commons_file),
            'thumbnail_url': self.get_thumbnail_url(wikimedia_commons_file),
        }
        
        # Get element in database if it exists
        wikimedia_commons_file = WikimediaCommonsFile.objects.filter(id=id).first()
        
        if not wikimedia_commons_file:
            # Creation
            pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsFile", target_object_id=id)
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
                if value != getattr(wikimedia_commons_file, field):
                    modified_fields[field] = value
            
            if modified_fields:
                # Modification
                pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsFile", target_object_id=id)
                pending_modification.action = PendingModification.MODIFY
                
                self.modified_objects = self.modified_objects + 1
                pending_modification.modified_fields = json.dumps(modified_fields)
                pending_modification.full_clean()
                pending_modification.save()
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete previous modification if any
                PendingModification.objects.filter(target_object_class="WikimediaCommonsFile", target_object_id=id).delete()
    
    def sync_wikimedia_commons_files(self):
        # Get wikimedia commons files
        files_to_fetch = []
        fetched_files = []
        
        files_to_fetch = WikimediaCommonsCategory.objects.exclude(main_image__exact='').values_list('main_image', flat=True)
        
        if not self.sync_only_main_image:
            files_list = WikimediaCommonsCategory.objects.exclude(files__exact='').values_list('files', flat=True)
            for files in files_list:
                files_to_fetch = files_to_fetch.extend(files.split(';'))
        
        print 'Requesting Wikimedia Commons...'
        files_to_fetch = list(set(files_to_fetch))
        total = len(files_to_fetch)
        count = 0
        max_count_per_request = 25
        for chunk in [files_to_fetch[i:i+max_count_per_request] for i in range(0,len(files_to_fetch),max_count_per_request)]:
            print str(count) + u'/' + str(total)
            count += len(chunk)
            
            files_result = self.request_wikimedia_commons_files(chunk)
            fetched_files.extend(files_result.keys())
            for title, wikimedia_commons_file in files_result.iteritems():
                self.handle_wikimedia_commons_file(title, wikimedia_commons_file)
        print str(count) + u'/' + str(total)
        
        # Delete pending creations if element was not downloaded
        PendingModification.objects.filter(target_object_class="WikimediaCommonsFile", action=PendingModification.CREATE).exclude(target_object_id__in=fetched_files).delete()
        
        # Look for deleted elements
        for wikimedia_commons_file in WikimediaCommonsFile.objects.exclude(id__in=fetched_files):
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsFile", target_object_id=wikimedia_commons_file.id)
            
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
            self.auto_apply = (Setting.objects.get(key=u'wikimedia_commons:auto_apply_modifications').value == 'true')
            self.sync_only_main_image = (Setting.objects.get(key=u'wikimedia_commons:sync_only_main_image').value == 'true')
            self.thumbnail_width = int(Setting.objects.get(key=u'wikimedia_commons:thumbnail_width').value)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_wikimedia_commons_files()
            
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
