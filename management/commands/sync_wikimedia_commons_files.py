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

import json, os, re, requests, sys, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from HTMLParser import HTMLParser

from superlachaise_api.models import *

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def print_unicode(str):
    print str.encode('utf-8')

def none_to_blank(s):
    if s is None:
        return u''
    return unicode(s)

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
                'iiprop': 'url|size|extmetadata',
                'format': 'json',
                'iiurlwidth': 50,
                'titles': titles,
            }
            params.update(last_continue)
            
            if settings.MEDIAWIKI_USER_AGENT:
                headers = {"User-Agent" : settings.MEDIAWIKI_USER_AGENT}
            else:
                raise 'no USER_AGENT defined in settings.py'
            
            json_result = requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers).json()
            
            if 'pages' in json_result['query']:
                for page_id, page in json_result['query']['pages'].iteritems():
                    result[page['title']] = page
            
            if 'continue' not in json_result: break
            
            last_continue = json_result['continue']
        
        return result
    
    def get_thumbnail_url(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return none_to_blank(image_info[0]['thumburl'])
        except:
            return u''
    
    def get_image_width(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return image_info[0]['width']
        except:
            return 0
    
    def get_original_url(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            
            return none_to_blank(image_info[0]['url'])
        except:
            return u''
    
    def get_author(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            extmetadata = image_info[0]['extmetadata']
            
            author = u''
            
            if not author and 'Artist' in extmetadata:
                author = strip_tags(extmetadata['Artist']['value'])
            
            # Extract derivative work
            match_obj = re.search(r'.*[Dd]erivative work:(.*)$', author)
            if match_obj:
                author = match_obj.group(1).strip()
            
            # Extract user
            match_obj = re.search(r'.*[Uu]ser:(.*)$', author)
            if match_obj:
                author = match_obj.group(1).strip()
            
            # Remove talk link
            author = author.replace('(talk)', '')
            
            # Remove new lines, strip
            author = author.replace('\n', ' ').strip()
            
            # Remove leading ~
            if len(author) > 1 and author[0] == '~':
                author = author[1:]
            
            # Remove multiple spaces
            while '  ' in author:
                author = author.replace('  ', ' ')
            
            return none_to_blank(author)
        except:
            return u''
    
    def get_license(self, wikimedia_commons_file):
        try:
            image_info = wikimedia_commons_file['imageinfo']
            if not len(image_info) == 1:
                raise BaseException
            extmetadata = image_info[0]['extmetadata']
            
            license_short_name = extmetadata['LicenseShortName']['value']
            
            return none_to_blank(license_short_name)
        except:
            return u''
    
    def handle_wikimedia_commons_file(self, id, wikimedia_commons_file):
        # Get values
        thumbnail_url = self.get_thumbnail_url(wikimedia_commons_file)
        original_url = self.get_original_url(wikimedia_commons_file)
        image_width = self.get_image_width(wikimedia_commons_file)
        
        values_dict = {}
        values_dict['author'] = self.get_author(wikimedia_commons_file)
        values_dict['license'] = self.get_license(wikimedia_commons_file)
        if image_width > 512:
            values_dict['url_512px'] = thumbnail_url.replace('50px-', '512px-')
        else:
            values_dict['url_512px'] = original_url
        if image_width > 1024:
            values_dict['url_1024px'] = thumbnail_url.replace('50px-', '1024px-')
        else:
            values_dict['url_1024px'] = original_url
        if image_width > 2048:
            values_dict['url_2048px'] = thumbnail_url.replace('50px-', '2048px-')
        else:
            values_dict['url_2048px'] = original_url
        
        # Get element in database if it exists
        target_object_id_dict = {"wikimedia_commons_id": id}
        wikimedia_commons_file, created = WikimediaCommonsFile.objects.get_or_create(**target_object_id_dict)
        self.fetched_objects_pks.append(wikimedia_commons_file.pk)
        modified = False
        
        if created:
            self.created_objects = self.created_objects + 1
        else:
            # Search for modifications
            for field, value in values_dict.iteritems():
                if value != getattr(wikimedia_commons_file, field):
                    modified = True
                    self.modified_objects = self.modified_objects + 1
                    break
        
        if created or modified:
            for field, value in values_dict.iteritems():
                setattr(wikimedia_commons_file, field, value)
            wikimedia_commons_file.save()
    
    def sync_wikimedia_commons_files(self, param_wikimedia_commons_files):
        # Get wikimedia commons files
        files_to_fetch = []
        self.fetched_objects_pks = []
        
        if param_wikimedia_commons_files:
            files_to_fetch = param_wikimedia_commons_files.split('|')
        else:
            files_to_fetch = []
            for wikimedia_commons_category in WikimediaCommonsCategory.objects.all():
                main_image = wikimedia_commons_category.main_image
                if main_image and not main_image in files_to_fetch:
                    files_to_fetch.append(main_image)
                category_members = wikimedia_commons_category.category_members
                if category_members:
                    for category_member in category_members.split('|'):
                        if not category_member in files_to_fetch:
                            files_to_fetch.append(category_member)
            files_to_fetch.extend(WikimediaCommonsCategory.objects.exclude(category_members__exact='').values_list('category_members', flat=True))
        
        print_unicode(_('Requesting Wikimedia Commons...'))
        files_to_fetch = list(set(files_to_fetch))
        total = len(files_to_fetch)
        count = 0
        max_count_per_request = 25
        for chunk in [files_to_fetch[i:i+max_count_per_request] for i in range(0,len(files_to_fetch),max_count_per_request)]:
            print_unicode(str(count) + u'/' + str(total))
            count += len(chunk)
            
            files_result = self.request_wikimedia_commons_files(chunk)
            for title, wikimedia_commons_file in files_result.iteritems():
                self.handle_wikimedia_commons_file(title, wikimedia_commons_file)
        print_unicode(str(count) + u'/' + str(total))
        
        if not param_wikimedia_commons_files:
            # Look for deleted elements
            for wikimedia_commons_file in WikimediaCommonsFile.objects.exclude(pk__in=self.fetched_objects_pks):
                self.deleted_objects = self.deleted_objects + 1
                wikimedia_commons_file.delete()
    
    def add_arguments(self, parser):
        parser.add_argument('--wikimedia_commons_files',
            action='store',
            dest='wikimedia_commons_files')
    
    def handle(self, *args, **options):
        
        try:
            self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0].split('sync_')[-1])
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            self.sync_wikimedia_commons_files(options['wikimedia_commons_files'])
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
