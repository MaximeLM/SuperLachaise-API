# -*- coding: utf-8 -*-

"""
write_diff_data.py
superlachaise_api

Created by Maxime Le Moine on 29/11/2015.
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

import json, os, sys
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.utils import formats, timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api import conf
from superlachaise_api.models import *
from superlachaise_api.views import *

def print_unicode(str):
    print str.encode('utf-8')

class Command(BaseCommand):
    
    def diff_json_dict(self, original_dict, updated_dict):
        diff = {}
        
        for key, value in updated_dict.iteritems():
            if not original_dict.has_key(key):
                diff[key] = value
        for key, value in original_dict.iteritems():
            if not updated_dict.has_key(key):
                diff[key] = None
            else:
                if isinstance(value, dict):
                    value_diff = self.diff_json_dict(value, updated_dict[key])
                    if value_diff:
                        diff[key] = value_diff
                elif isinstance(value, list):
                    value_diff = self.diff_json_list(key, value, updated_dict[key])
                    if value_diff != None:
                        diff[key] = value_diff
                else:
                    if value != updated_dict[key]:
                        diff[key] = updated_dict[key]
        
        return diff
    
    def diff_json_list(self, list_name, original_list, updated_list):
        original_dict = {}
        updated_dict = {}
        for object in original_list:
            original_dict[self.key_for_object(list_name, object)] = object
        for object in updated_list:
            updated_dict[self.key_for_object(list_name, object)] = object
        
        diff_dict = self.diff_json_dict(original_dict, updated_dict)
        
        return self.diff_list_for_diff_dict(list_name, diff_dict, updated_list)
    
    def key_for_object(self, list_name, object):
        if list_name == 'openstreetmap_elements':
            return object['openstreetmap_id']
        elif list_name == 'superlachaise_categories' and isinstance(object, dict):
            return object['code']
        elif list_name == 'superlachaise_pois':
            return object['id']
        elif list_name == 'wikidata_entries':
            return object['wikidata_id']
        elif list_name == 'wikimedia_commons_categories':
            return object['wikimedia_commons_id']
        elif list_name == 'localizations':
            return object['id']
        elif list_name == 'category_members':
            return object
        elif list_name == 'superlachaise_categories':
            return object
        elif list_name == 'persons':
            return object
        elif list_name == 'others':
            return object
        elif list_name == 'artists':
            return object
        else:
            raise CommandError(_(u'Unknown list name: ' + list_name))
    
    def diff_list_for_diff_dict(self, list_name, diff_dict, updated_list):
        if not diff_dict:
            return None
        
        diff_list = []
        for key, value in diff_dict.iteritems():
            if value is None:
                diffValue = { "deleted": True }
            else:
                diffValue = value
            if list_name == 'openstreetmap_elements':
                diffValue['openstreetmap_id'] = key
                diff_list.append(diffValue)
            elif list_name == 'superlachaise_categories' and isinstance(value, dict):
                diffValue['code'] = key
                diff_list.append(diffValue)
            elif list_name == 'superlachaise_pois':
                diffValue['id'] = key
                diff_list.append(diffValue)
            elif list_name == 'wikidata_entries':
                diffValue['wikidata_id'] = key
                diff_list.append(diffValue)
            elif list_name == 'wikimedia_commons_categories':
                diffValue['wikimedia_commons_id'] = key
                diff_list.append(diffValue)
            else:
                diff_list = updated_list
        
        if list_name == 'localizations':
            localizations_diff = []
            for diff in diff_list:
                if diff_dict.has_key(diff['id']):
                    diff_dict[diff['id']]['id'] = diff['id']
                    localizations_diff.append(diff_dict[diff['id']])
                else:
                    localizations_diff.append({
                        'id': diff['id']
                    })
            diff_list = localizations_diff
        
        return diff_list
    
    def apply_diff_dict(self, original_dict, diff_dict):
        for key, value in diff_dict.iteritems():
            if isinstance(value, dict):
                original_dict[key] = self.apply_diff_dict(original_dict[key], value)
            elif isinstance(value, list):
                original_dict[key] = self.apply_diff_list(key, original_dict[key], value)
            else:
                original_dict[key] = value
        
        return original_dict
    
    def apply_diff_list(self, list_name, original_list, diff_list):
        if list_name in [
            'openstreetmap_elements', 'superlachaise_categories', 'superlachaise_pois', 'wikidata_entries', 'wikimedia_commons_categories']:
            original_dict = {}
            for object in original_list:
                original_dict[self.key_for_object(list_name, object)] = object
            for diff in diff_list:
                original_dict[self.key_for_object(list_name, diff)] = self.apply_diff_dict(original_dict[self.key_for_object(list_name, diff)], diff)
            return original_list
        elif list_name == 'localizations':
            original_dict = {}
            for object in original_list:
                original_dict[self.key_for_object(list_name, object)] = object
            updated_list = []
            for diff in diff_list:
                updated_dict = self.apply_diff_dict(original_dict[diff['id']], diff)
                updated_list.append(updated_dict)
            return updated_list
        else:
            return diff_list
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        try:
            # Compute file path
            currentVersion = DBVersion.objects.all().aggregate(Max('version_id'))['version_id__max']
            if not currentVersion:
                raise CommandError(_(u'No DB version found'))
            diff_file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_diff_" + str(currentVersion-1) + "-" + str(currentVersion) + ".json"
            if os.path.isfile(diff_file_path):
                raise CommandError(_(u'A diff file for this version already exists: ') + diff_file_path)
        
            previous_full_file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_full_" + str(currentVersion-1) + ".json"
            if not os.path.isfile(previous_full_file_path):
                raise CommandError(_(u'The full file for the previous version does not exist: ') + previous_full_file_path)
        
            current_full_file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_full_" + str(currentVersion) + ".json"
            if not os.path.isfile(current_full_file_path):
                raise CommandError(_(u'The full file for the current version does not exist: ') + current_full_file_path)
        
            with open(previous_full_file_path) as previous_full_file:    
                previous_full_data = json.load(previous_full_file)
        
            with open(current_full_file_path) as current_full_file:    
                current_full_data = json.load(current_full_file)
        
            diff_dict = self.diff_json_dict(previous_full_data, current_full_data)
        
            # Assert that the diff dict applied to the previous file is equal to the current file
            with open(previous_full_file_path) as previous_full_file:    
                previous_full_data = json.load(previous_full_file)
        
            with open(current_full_file_path) as current_full_file:    
                current_full_data = json.load(current_full_file)
        
            updated_previous_data = self.apply_diff_dict(previous_full_data, diff_dict)
        
            error_file_path = diff_file_path.replace('.json', '-error.json')
            if updated_previous_data != current_full_data:
                with open(error_file_path, 'w') as error_file:
                    error_file.write(json.dumps(updated_previous_data, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True).encode('utf8'))
                raise CommandError(_(u'The diff file is incorrect'))
            elif os.path.isfile(error_file_path):
                os.remove(error_file_path)
        
            diff_dict['about'] = {
                'licence': "https://api.superlachaise.fr/perelachaise/api/licence/",
                'api_version': conf.VERSION,
                'db_version': str(currentVersion-1) + "-" + str(currentVersion),
                'type': 'diff',
            }
            
            for key in ['openstreetmap_elements', 'wikidata_entries', 'wikimedia_commons_categories', 'superlachaise_categories', 'superlachaise_pois']:
                if not diff_dict.has_key(key):
                    diff_dict[key] = []
        
            with open(diff_file_path, 'w') as diff_file:
                diff_file.write(json.dumps(diff_dict, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True).encode('utf8'))
        except:
            print_unicode(traceback.format_exc())
            translation.deactivate()
            raise CommandError(sys.exc_info()[1])
        translation.deactivate()
