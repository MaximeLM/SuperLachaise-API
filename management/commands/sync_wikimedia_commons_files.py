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

import json, os, re, sys, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def request_wikimedia_commons_files(self, wikimedia_commons_files):
        max_items_per_request = 10
        
        result = {}
        i = 0
        while i < len(wikimedia_commons_files):
            rawcontinue = '&rawcontinue'
            
            wikimedia_commons_files_page = wikimedia_commons_files[i : min(len(wikimedia_commons_files), i + max_items_per_request)]
            
            while rawcontinue:
                # Request properties
                url = "http://commons.wikimedia.org/w/api.php?action=query&titles={titles}&prop=imageinfo&iiprop=url&iiurlwidth={thumbnail_size}{rawcontinue}&format=json"\
                    .format(titles=urllib2.quote('|'.join(wikimedia_commons_files_page).encode('utf8'), '|'), rawcontinue=rawcontinue, thumbnail_size=self.thumbnail_width)
                
                request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
                u = urllib2.urlopen(request)
                
                # Parse result
                data = u.read()
                json_result = json.loads(data)
                
                for page_id, page in json_result['query']['pages'].iteritems():
                    result[page['title']] = page
            
                if 'query-continue' in json_result and 'pages' in json_result['query-continue']:
                    rawcontinue = '&rawcontinue=%s' % (json_result['query-continue']['continue']['rawcontinue'])
                else:
                    rawcontinue = u''
            
            i = i + max_items_per_request
        
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
                pending_modification = PendingModification.objects.filter(target_object_class="WikimediaCommonsFile", target_object_id=id).first()
                if pending_modification:
                    pending_modification.delete()
    
    def sync_wikimedia_commons_files(self):
        # Get wikimedia commons files
        fetched_files = []
        count = WikimediaCommonsCategory.objects.count()
        for wikimedia_commons_category in WikimediaCommonsCategory.objects.all():
            print str(count) + u'-' + unicode(wikimedia_commons_category)
            count -= 1
            wikimedia_commons_files = []
            if wikimedia_commons_category.main_image:
                if not wikimedia_commons_category.main_image in wikimedia_commons_files:
                    wikimedia_commons_files.append(wikimedia_commons_category.main_image)
            if not self.sync_only_main_image and self.wikimedia_commons_category.files:
                for link in wikimedia_commons_category.files.split(';'):
                    if not link in wikimedia_commons_files:
                        wikimedia_commons_files.append(link)
            
            files_result = self.request_wikimedia_commons_files(wikimedia_commons_files)
            for title, wikimedia_commons_file in files_result.iteritems():
                fetched_files.append(title)
                self.handle_wikimedia_commons_file(title, wikimedia_commons_file)
        
        # Delete pending creations if element was not downloaded
        for pendingModification in PendingModification.objects.filter(target_object_class="WikimediaCommonsFile", action=PendingModification.CREATE):
            if not pendingModification.target_object_id in fetched_files:
                pendingModification.delete()
        
        # Look for deleted elements
        for wikimedia_commons_file in WikimediaCommonsFile.objects.all():
            if not wikimedia_commons_file.id in fetched_files:
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
