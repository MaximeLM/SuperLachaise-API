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
        max_items_per_request = 100
        
        result = {}
        i = 0
        while i < len(wikimedia_commons_files):
            rawcontinue = '&rawcontinue'
            
            wikimedia_commons_files_page = wikimedia_commons_files[i : min(len(wikimedia_commons_files), i + max_items_per_request)]
            
            while rawcontinue:
                # Request properties
                url = "http://commons.wikimedia.org/w/api.php?action=query&titles={titles}&prop=imageinfo|revisions&iiprop=extmetadata|url|size&iiurlwidth={thumbnail_size}&rvprop=content{rawcontinue}&format=json"\
                    .format(titles=urllib2.quote('|'.join(wikimedia_commons_files).encode('utf8'), '|'), rawcontinue=rawcontinue, thumbnail_size=self.placeholder_thumbnail_size)
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
    
    def get_thumbnail_template_url(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            thumbnail_url = image_info[0]['thumburl']
            
            return thumbnail_url.replace(u'/' + self.placeholder_thumbnail_size + 'px', u'/{{width}}px')
        except:
            return u''
    
    def get_size(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return (image_info[0]['width'], image_info[0]['height'])
        except:
            return (None, None)
    
    def get_attribution(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            licence_short_name = image_info[0]['extmetadata']['LicenseShortName']['value']
            
            revisions = wikimedia_commons_file['revisions']
            if not len(revisions) == 1:
                raise BaseException
            
            wikitext = revisions[0]['*']
            for line in wikitext.split('\n'):
                match_obj = re.search( r'^.*[aA]uthor.*\[\[User:.*\|(.*)\]\].*$', line)
                if match_obj:
                    author = match_obj.group(1).strip()
                    break
            
            if not licence_short_name or not author:
                raise BaseException
            
            return u'{author} / Wikimedia Commons / {licence}'.format(author=author, licence=licence_short_name)
        except:
            traceback.print_exc()
            return u''
    
    def handle_wikimedia_commons_file(self, id, wikimedia_commons_file):
        # Get data
        values_dict = {
            'original_url': self.get_original_url(wikimedia_commons_file),
            'thumbnail_template_url': self.get_thumbnail_template_url(wikimedia_commons_file),
            'attribution': self.get_attribution(wikimedia_commons_file),
        }
        values_dict['width'], values_dict['height'] = self.get_size(wikimedia_commons_file)
        
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
        wikimedia_commons_files = []
        for wikimedia_commons_category in WikimediaCommonsCategory.objects.all():
            if wikimedia_commons_category.files:
                for link in wikimedia_commons_category.files.split(';'):
                    if not link in wikimedia_commons_files:
                        wikimedia_commons_files.append(link)
        
        result = self.request_wikimedia_commons_files(wikimedia_commons_files)
        
        count = len(result)
        for title, wikimedia_commons_file in result.iteritems():
            print str(count) + u'-' + title
            count = count - 1
            self.handle_wikimedia_commons_file(title, wikimedia_commons_file)
        
        # Delete pending creations if element was not downloaded
        for pendingModification in PendingModification.objects.filter(target_object_class="WikimediaCommonsFile", action=PendingModification.CREATE):
            if not pendingModification.target_object_id in result:
                pendingModification.delete()
        
        # Look for deleted elements
        for wikimedia_commons_file in WikimediaCommonsFile.objects.all():
            if not wikimedia_commons_file.id in result:
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
            self.auto_apply = (Setting.objects.get(category='Wikimedia Commons', key=u'auto_apply_modifications').value == 'true')
            self.placeholder_thumbnail_size = u'350'
            
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
