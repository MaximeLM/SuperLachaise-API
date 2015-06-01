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

import json, os, sys, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def request_image_list(self, wikimedia_commons_category):
        result = []
        should_continue = True
        cmcontinue = ''
        
        while should_continue:
            # Request properties
            url = "http://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtype=file&rawcontinue&format=json&cmtitle=Category:{category}{cmcontinue}"\
                .format(category=urllib2.quote(wikimedia_commons_category.encode('utf8')), cmcontinue=cmcontinue)
            request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
            u = urllib2.urlopen(request)
            
            # Parse result
            data = u.read()
            json_result = json.loads(data)
            
            for image in json_result['query']['categorymembers']:
                result.append(image['title'])
            
            if 'query-continue' in json_result:
                cmcontinue = '&cmcontinue=%s' % (json_result['query-continue']['categorymembers']['cmcontinue'])
            else:
                should_continue = False
        
        return result
    
    def handle_wikimedia_commons_category(self, id):
        # Get images
        values_dict = {
            'files': ';'.join(self.request_image_list(id))
        }
        
        # Get element in database if it exists
        wikimedia_commons_category = WikimediaCommonsCategory.objects.filter(id=id).first()
        
        if not wikimedia_commons_category:
            # Creation
            pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=id)
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
                if value != getattr(wikimedia_commons_category, field):
                    modified_fields[field] = value
            
            if modified_fields:
                # Modification
                pending_modification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=id)
                pending_modification.action = PendingModification.MODIFY
                
                self.modified_objects = self.modified_objects + 1
                pending_modification.modified_fields = json.dumps(modified_fields)
                pending_modification.full_clean()
                pending_modification.save()
                
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete previous modification if any
                pending_modification = PendingModification.objects.filter(target_object_class="WikimediaCommonsCategory", target_object_id=id).first()
                if pending_modification:
                    pending_modification.delete()
    
    def sync_wikimedia_commons_categories(self):
        # Get wikimedia commons categories
        wikimedia_commons_categories = []
        for openstreetmap_element in OpenStreetMapElement.objects.all():
            if openstreetmap_element.wikimedia_commons and openstreetmap_element.wikimedia_commons.startswith('Category:'):
                link = openstreetmap_element.wikimedia_commons.split('Category:')[1]
                if not link in wikimedia_commons_categories:
                    wikimedia_commons_categories.append(link)
        for wikidata_entry in WikidataEntry.objects.all():
            if wikidata_entry.wikimedia_commons_category:
                sync_category = False
                for instance_of in wikidata_entry.instance_of.split(';'):
                    if instance_of in self.synced_instance_of:
                        sync_category = True
                        break
                if sync_category:
                    link = wikidata_entry.wikimedia_commons_category
                    if not link in wikimedia_commons_categories:
                        wikimedia_commons_categories.append(link)
            if wikidata_entry.wikimedia_commons_grave_category:
                link = wikidata_entry.wikimedia_commons_grave_category
                if not link in wikimedia_commons_categories:
                    wikimedia_commons_categories.append(link)
        
        count = len(wikimedia_commons_categories)
        for wikimedia_commons_category in wikimedia_commons_categories:
            print str(count) + u'-' + wikimedia_commons_category
            count = count - 1
            self.handle_wikimedia_commons_category(wikimedia_commons_category)
        
        # Delete pending creations if element was not downloaded
        for pendingModification in PendingModification.objects.filter(target_object_class="WikimediaCommonsCategory", action=PendingModification.CREATE):
            if not pendingModification.target_object_id in wikimedia_commons_categories:
                pendingModification.delete()
        
        # Look for deleted elements
        for wikimedia_commons_category in WikimediaCommonsCategory.objects.all():
            if not wikimedia_commons_category.id in wikimedia_commons_categories:
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikimediaCommonsCategory", target_object_id=wikimedia_commons_category.id)
                
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
            self.synced_instance_of = json.loads(Setting.objects.get(category='Wikimedia Commons', key=u'synced_instance_of').value)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_wikimedia_commons_categories()
            
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
