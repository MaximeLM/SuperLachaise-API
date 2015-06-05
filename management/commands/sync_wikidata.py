# -*- coding: utf-8 -*-

"""
sync_wikidata.py
superlachaise_api

Created by Maxime Le Moine on 28/05/2015.
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

import datetime, json, os, sys, time, traceback, urllib2
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from HTMLParser import HTMLParser

from superlachaise_api.models import *

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def none_to_blank(s):
    if s is None:
        return u''
    return unicode(s)

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
    
    def request_wikipedia_pre_section(self, language_code, title):
        # Request properties
        url = "http://{language_code}.wikipedia.org/w/api.php?action=parse&page={title}&format=json&prop=text&section=0"\
            .format(language_code=language_code, title=urllib2.quote(title.encode('utf8')))
        request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
        u = urllib2.urlopen(request)
        
        # Parse result
        data = u.read()
        json_result = json.loads(data)
        
        return json_result['parse']['text']['*']
    
    def get_wikipedia_intro(self, language_code, title):
        # Get wikipedia pre-section (intro)
        pre_section = self.request_wikipedia_pre_section(language_code, title)
        
        # Process HTML
        parser = WikipediaIntroHTMLParser(language_code)
        parser.feed(pre_section)
        
        return parser.get_data()
    
    def request_wikidata(self, wikidata_codes):
        # List languages to request
        languages = []
        for language in Language.objects.all():
            languages.append(language.code)
        
        # List props to request
        props = ['labels', 'descriptions', 'claims', 'sitelinks']
        
        max_items_per_request = 25
        
        result = {}
        i = 0
        while i < len(wikidata_codes):
            wikidata_codes_page = wikidata_codes[i : min(len(wikidata_codes), i + max_items_per_request)]
            
            # Request properties
            url = "http://www.wikidata.org/w/api.php?languages={languages}&action=wbgetentities&ids={ids}&props={props}&format=json"\
                .format(languages='|'.join(languages), ids='|'.join(wikidata_codes_page), props='|'.join(props))
            request = urllib2.Request(url, headers={"User-Agent" : "SuperLachaise API superlachaise@gmail.com"})
            u = urllib2.urlopen(request)
            
            # Parse result
            data = u.read()
            json_result = json.loads(data)
            
            # Add entities to result
            result.update(json_result['entities'])
            
            i = i + max_items_per_request
        
        return result
    
    def get_instance_of(self, entity):
        try:
            p31 = entity['claims']['P31']
            
            result = []
            for entry in p31:
                result.append('Q' + str(entry['mainsnak']['datavalue']['value']['numeric-id']))
            
            return result
        except:
            return []
    
    def get_occupations(self, entity):
        try:
            p106 = entity['claims']['P106']
            
            result = []
            for entry in p106:
                result.append('Q' + str(entry['mainsnak']['datavalue']['value']['numeric-id']))
            
            return result
        except:
            return []
    
    def get_sex_or_gender(self, entity):
        try:
            p31 = entity['claims']['P21']
            
            result = []
            if len(p31) == 1:
                result = 'Q' + str(p31[0]['mainsnak']['datavalue']['value']['numeric-id'])
            
            return result
        except:
            return []
    
    def get_wikimedia_commons_category(self, entity):
        try:
            # Use P373
            p373 = entity['claims']['P373']
            
            wikimedia_commons = p373[0]['mainsnak']['datavalue']['value']
            
            # Delete random trailing character
            return wikimedia_commons.replace(u'\u200e',u'')
        except:
            return u''
    
    def get_wikimedia_commons_grave_category(self, entity):
        try:
            p119 = entity['claims']['P119']
            
            for location_of_burial in p119:
                if ('Q' + str(location_of_burial['mainsnak']['datavalue']['value']['numeric-id'])) in self.accepted_locations_of_burial:
                    p373 = location_of_burial['qualifiers']['P373']
                    break
            
            wikimedia_commons = p373[0]['datavalue']['value']
            
            # Delete random trailing character
            return wikimedia_commons.replace(u'\u200e',u'')
        except:
            return u''
    
    def get_date(self, entity, date_code):
        try:
            date = entity['claims'][date_code]
            
            date_value = date[0]['mainsnak']['datavalue']['value']
            
            precision_string = date_value['precision']
            date_string = date_value['time']
            
            date = datetime.date(*time.strptime(date_string[1:11], "%Y-%m-%d")[:3])
            
            # Convert accuracy
            if precision_string == 9:
                accuracy = WikidataEntry.YEAR
            elif precision_string == 10:
                accuracy = WikidataEntry.MONTH
            elif precision_string == 11:
                accuracy = WikidataEntry.DAY
            else:
                raise BaseException
            
            return (date, accuracy)
        except:
            return (None, u'')
    
    def get_name(self, entity, language_code):
        try:
            name = entity['labels'][language_code]
            
            return name['value']
        except:
            return u''
    
    def get_wikipedia(self, entity, language_code):
        try:
            wikipedia = entity['sitelinks'][language_code + 'wiki']
            
            return wikipedia['title']
        except:
            return u''
    
    def get_description(self, entity, language_code):
        try:
            description = entity['descriptions'][language_code]
            
            return description['value']
        except:
            return u''
    
    def get_grave_of_wikidata(self, entity):
        try:
            p31 = entity['claims']['P31']
            
            result = []
            for entry in p31:
                if str(entry['mainsnak']['datavalue']['value']['numeric-id']) == '173387':
                    for p642 in entry['qualifiers']['P642']:
                        result.append('Q' + str(p642['datavalue']['value']['numeric-id']))
                    break
            
            return result
        except:
            return None
    
    def get_person_burial_plot_reference(self, entity):
        try:
            p119 = entity['claims']['P119']
            
            for location_of_burial in p119:
                if ('Q' + str(location_of_burial['mainsnak']['datavalue']['value']['numeric-id'])) in self.accepted_locations_of_burial:
                    p965 = location_of_burial['qualifiers']['P965']
                    break
            
            return p965[0]['datavalue']['value']
        except:
            return u''
    
    def get_burial_plot_reference(self, entity):
        try:
            p965 = entity['claims']['P965']
            
            return p965[0]['mainsnak']['datavalue']['value']
        except:
            return u''
    
    def get_field_of_profession(self, entity):
        try:
            p965 = entity['claims']['P965']
            
            return p965[0]['mainsnak']['datavalue']['value']
        except:
            return u''
    
    def get_values_from_entity(self, entity):
        result = {}
        
        instance_of = self.get_instance_of(entity)
        result['instance_of'] = ';'.join(instance_of)
        
        result['wikimedia_commons_category'] = self.get_wikimedia_commons_category(entity)
        
        if 'Q5' in instance_of:
            # human
            result['wikimedia_commons_grave_category'] = self.get_wikimedia_commons_grave_category(entity)
            result['burial_plot_reference'] = self.get_person_burial_plot_reference(entity)
            result['date_of_birth'], result['date_of_birth_accuracy'] = self.get_date(entity, 'P569')
            result['date_of_death'], result['date_of_death_accuracy'] = self.get_date(entity, 'P570')
            result['sex_or_gender'] = self.get_sex_or_gender(entity)
            result['occupations'] = ';'.join(self.get_occupations(entity))
        else:
            result['wikimedia_commons_grave_category'] = u''
            result['burial_plot_reference'] = self.get_burial_plot_reference(entity)
            result['date_of_birth'], result['date_of_birth_accuracy'] = (None, u'')
            result['date_of_death'], result['date_of_death_accuracy'] = (None, u'')
            result['sex_or_gender'] = u''
            result['occupations'] = u''
        
        if 'Q173387' in instance_of:
            # tomb
            grave_of_wikidata = self.get_grave_of_wikidata(entity)
            if grave_of_wikidata:
                for grave_of in grave_of_wikidata:
                    if not grave_of in self.wikidata_codes and not grave_of in self.grave_of_wikidata_codes:
                        self.grave_of_wikidata_codes.append(grave_of)
                result['grave_of_wikidata'] = ';'.join(grave_of_wikidata)
            else:
                result['grave_of_wikidata'] = u''
        else:
            result['grave_of_wikidata'] = u''
        
        return result
    
    def get_localized_values_from_entity(self, entity, language_code):
        wikipedia = self.get_wikipedia(entity, language_code)
        result = {
            language_code + ':name': self.get_name(entity, language_code),
            language_code + ':wikipedia': wikipedia,
            language_code + ':description': self.get_description(entity, language_code),
        }
        if wikipedia:
            result[language_code + ':intro'] = self.get_wikipedia_intro(language_code, wikipedia)
        
        for key, value in result.iteritems():
            if value != u'' and not value is None:
                return result
        
        return None
    
    def handle_entity(self, code, entity):
        # Get element in database if it exists
        wikidata_entry = WikidataEntry.objects.filter(id=code).first()
        
        if not wikidata_entry:
            # Creation
            pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=code)
            
            values_dict = self.get_values_from_entity(entity)
            for language in Language.objects.all():
                localized_values_dict = self.get_localized_values_from_entity(entity, language.code)
                if localized_values_dict:
                    values_dict.update(localized_values_dict)
            
            pendingModification.action = PendingModification.CREATE
            pendingModification.modified_fields = json.dumps(values_dict, default=date_handler)
            
            pendingModification.full_clean()
            pendingModification.save()
            self.created_objects = self.created_objects + 1
            
            if self.auto_apply:
                pendingModification.apply_modification()
        else:
            # Search for modifications
            modified_values = {}
            
            values_dict = self.get_values_from_entity(entity)
            for field, value in values_dict.iteritems():
                if value != getattr(wikidata_entry, field):
                    modified_values[field] = value
            
            for language in Language.objects.all():
                values_dict = self.get_localized_values_from_entity(entity, language.code)
                wikidata_localized_entry = wikidata_entry.localizations.filter(language=language).first()
                
                if values_dict:
                    if not wikidata_localized_entry:
                        modified_values.update(values_dict)
                    else:
                        for field, value in values_dict.iteritems():
                            if value != getattr(wikidata_localized_entry, field.split(':')[1]):
                                modified_values[field] = value
                else:
                    if wikidata_localized_entry:
                        modified_values[language.code + u':'] = None
            
            if modified_values:
                # Get or create a modification
                pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=code)
                pendingModification.modified_fields = json.dumps(modified_values, default=date_handler)
                pendingModification.action = PendingModification.MODIFY
            
                pendingModification.full_clean()
                pendingModification.save()
                self.modified_objects = self.modified_objects + 1
            
                if self.auto_apply:
                    pendingModification.apply_modification()
            else:
                # Delete the previous modification if any
                pendingModification = PendingModification.objects.filter(target_object_class="WikidataEntry", target_object_id=code).first()
                if pendingModification:
                    pendingModification.delete()
    
    def sync_wikidata(self, wikidata_ids):
        self.wikidata_codes = []
        
        # List wikidata codes and/or wikipedia titles in openstreetmap objects
        if wikidata_ids:
            self.wikidata_codes = wikidata_ids.split('|')
        else:
            for openstreetmap_element in OpenStreetMapElement.objects.all():
                if openstreetmap_element.wikidata_combined:
                    for wikidata in openstreetmap_element.wikidata_combined.split(';'):
                        link = wikidata.split(':')[-1]
                        if not link in self.wikidata_codes:
                            self.wikidata_codes.append(link)
            for wikidata_entry in WikidataEntry.objects.all():
                if wikidata_entry.grave_of_wikidata:
                    for link in wikidata_entry.grave_of_wikidata.split(';'):
                        if not link in self.wikidata_codes:
                            self.wikidata_codes.append(link)
        
        # Request wikidata entities
        entities = {}
        if self.wikidata_codes:
            entities.update(self.request_wikidata(self.wikidata_codes))
        
        count = len(entities)
        self.grave_of_wikidata_codes = []
        for code, entity in entities.iteritems():
            print str(count) + u'-' + code
            count -= 1
            self.handle_entity(code, entity)
        
        # Request grave of entities
        grave_of_entities = {}
        if self.grave_of_wikidata_codes:
            grave_of_entities.update(self.request_wikidata(self.grave_of_wikidata_codes))
            entities.update(grave_of_entities)
        
        count = len(grave_of_entities)
        for code, entity in grave_of_entities.iteritems():
            print u'grave-' + str(count) + u'-' + code
            count -= 1
            self.handle_entity(code, entity)
        
        if not wikidata_ids:
            # Delete pending creations if element was deleted in Wikidata
            for pendingModification in PendingModification.objects.filter(target_object_class="WikidataEntry", action=PendingModification.CREATE):
                if not pendingModification.target_object_id in entities:
                    pendingModification.delete()
        
            # Look for deleted elements
            for wikidata_entry in WikidataEntry.objects.all():
                if not wikidata_entry.id in entities:
                    pendingModification, created = PendingModification.objects.get_or_create(target_object_class="WikidataEntry", target_object_id=wikidata_entry.id)
                
                    pendingModification.action = PendingModification.DELETE
                    pendingModification.modified_fields = u''
                
                    pendingModification.full_clean()
                    pendingModification.save()
                    self.deleted_objects = self.deleted_objects + 1
                
                    if self.auto_apply:
                        pendingModification.apply_modification()
    
    def add_arguments(self, parser):
        parser.add_argument('--wikidata_ids',
            action='store',
            dest='wikidata_ids')
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        try:
            self.accepted_locations_of_burial = json.loads(Setting.objects.get(key=u'wikidata:accepted_locations_of_burial').value)
            self.auto_apply = (Setting.objects.get(key=u'wikidata:auto_apply_modifications').value == 'true')
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            
            self.sync_wikidata(options['wikidata_ids'])
            
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
