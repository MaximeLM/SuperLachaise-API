# -*- coding: utf-8 -*-

"""
views.py
superlachaise_api

Created by Maxime Le Moine on 05/06/2015.
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

import datetime, json, os
from decimal import Decimal
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_http_methods
from django.utils import encoding, timezone, dateparse
from django.utils.translation import ugettext as _

from superlachaise_api import conf
from superlachaise_api.models import *

class SuperLachaiseEncoder(object):
    
    def __init__(self, request, languages=None, restrict_fields=True):
        self.request = request
        self.languages = languages
        self.restrict_fields = restrict_fields
    
    def encode(self, obj):
        obj['about'] = self.about_dict()
        return json.dumps(self.obj_dict(obj), ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, default=self.default)
    
    def about_dict(self):
        result = {
            'licence': self.request.build_absolute_uri(reverse(licence)),
            'source': self.request.build_absolute_uri(reverse(objects)),
            'version': conf.VERSION,
        }
        
        return result
    
    def default(self, obj):
        if isinstance(obj, datetime.date):
            result = obj.isoformat()
        elif isinstance(obj, Decimal):
            if obj == 0:
                result = "0"
            else:
                result = str(obj)
        elif isinstance(obj, basestring):
            result = obj
        else:
            result = None
        return result
    
    def obj_dict(self, obj):
        if isinstance(obj, Page):
            return self.page_dict(obj)
        elif isinstance(obj, SuperLachaisePOI):
            return self.superlachaise_poi_dict(obj)
        elif isinstance(obj, SuperLachaiseCategory):
            return self.superlachaise_category_dict(obj)
        elif isinstance(obj, OpenStreetMapElement):
            return self.openstreetmap_element_dict(obj)
        elif isinstance(obj, WikidataEntry):
            return self.wikidata_entry_dict(obj)
        elif isinstance(obj, WikimediaCommonsCategory):
            return self.wikimedia_commons_category_dict(obj)
        elif isinstance(obj, list) or isinstance(obj, QuerySet):
            return [self.obj_dict(list_item) for list_item in obj]
        elif isinstance(obj, dict):
            return {self.obj_dict(key): self.obj_dict(value) for key, value in obj.iteritems()}
        else:
            return obj
    
    def page_dict(self, page):
        result = {
            'current_page': page.number,
            'number_of_results_on_page': len(page.object_list),
            'number_of_pages': page.paginator.num_pages,
            'number_of_results': page.paginator.count,
        }
        
        if page.has_previous():
            params = self.request.GET.copy()
            params['page'] = page.previous_page_number()
            page_path = u'{path}?{params}'.format(path=self.request.path, params='&'.join(['%s=%s' % (key, value) for key, value in params.iteritems()]))
            
            result.update({
                'previous_page': params['page'],
                'previous_page_url': self.request.build_absolute_uri(page_path.replace(' ', '+')),
            })
        
        if page.has_next():
            params = self.request.GET.copy()
            params['page'] = page.next_page_number()
            page_path = u'{path}?{params}'.format(path=self.request.path, params='&'.join(['%s=%s' % (key, value) for key, value in params.iteritems()]))
            
            result.update({
                'next_page': params['page'],
                'next_page_url': self.request.build_absolute_uri(page_path.replace(' ', '+')),
            })
        
        return result
    
    def superlachaise_poi_dict(self, superlachaise_poi):
        if superlachaise_poi.deleted:
            result = {
                'id': superlachaise_poi.pk,
                'deleted': superlachaise_poi.deleted,
            }
        else:
            result = {
                'id': superlachaise_poi.pk,
                'burial_plot_reference': superlachaise_poi.burial_plot_reference,
                'date_of_birth': superlachaise_poi.date_of_birth,
                'date_of_birth_accuracy': superlachaise_poi.date_of_birth_accuracy,
                'date_of_death': superlachaise_poi.date_of_death,
                'date_of_death_accuracy': superlachaise_poi.date_of_death_accuracy,
            }
        
            localizations = []
            if self.languages:
                for language in self.languages:
                    superlachaise_localized_poi = superlachaise_poi.localizations.filter(language=language).first()
                    if superlachaise_localized_poi:
                        localizations.append({
                            'id': superlachaise_localized_poi.pk,
                            'language_code': language.code,
                            'name': superlachaise_localized_poi.name,
                            'sorting_name': superlachaise_localized_poi.sorting_name,
                            'description': superlachaise_localized_poi.description,
                        })
        
            wikidata_entry_relations = {}
            for wikidata_entry_relation in superlachaise_poi.superlachaisewikidatarelation_set.all():
                if not wikidata_entry_relation.relation_type in wikidata_entry_relations:
                    wikidata_entry_relations[wikidata_entry_relation.relation_type] = []
                wikidata_entry_relations[wikidata_entry_relation.relation_type].append(wikidata_entry_relation.wikidata_entry.wikidata_id)
        
            superlachaise_categories = superlachaise_poi.superlachaise_categories.all().values_list('code', flat=True)
            
            if superlachaise_poi.openstreetmap_element:
                result['openstreetmap_element'] = {
                    'openstreetmap_id': superlachaise_poi.openstreetmap_element.openstreetmap_id,
                    'type': superlachaise_poi.openstreetmap_element.type,
                }
            else:
                result['openstreetmap_element'] = None
            
            if superlachaise_poi.wikimedia_commons_category:
                result['wikimedia_commons_category'] = superlachaise_poi.wikimedia_commons_category.wikimedia_commons_id
            else:
                result['wikimedia_commons_category'] = None
            
            result.update({
                'localizations': localizations,
                'wikidata_entries': wikidata_entry_relations,
                'superlachaise_categories': self.obj_dict(superlachaise_categories),
            })
        
        return result
    
    def superlachaise_category_dict(self, superlachaise_category):
        if superlachaise_category.deleted:
            result = {
                'code': superlachaise_category.code,
                'deleted': superlachaise_category.deleted,
            }
        else:
            result = {
                'code': superlachaise_category.code,
                'type': superlachaise_category.type,
            }
        
            localizations = []
            if self.languages:
                for language in self.languages:
                    superlachaise_localized_category = superlachaise_category.localizations.filter(language=language).first()
                    if superlachaise_localized_category:
                        localizations.append({
                            'id': superlachaise_localized_category.pk,
                            'language_code': language.code,
                            'name': superlachaise_localized_category.name,
                        })
            result['localizations'] = localizations
        
            if not self.restrict_fields:
                result.update({
                    'wikidata_occupations': ['Q%s' % wikidata_occupation.id for wikidata_occupation in superlachaise_category.wikidata_occupations.all()],
                })
        
        return result
    
    def openstreetmap_element_dict(self, openstreetmap_element):
        if openstreetmap_element.deleted:
            result = {
                'openstreetmap_id': openstreetmap_element.openstreetmap_id,
                'type': openstreetmap_element.type,
                'deleted': openstreetmap_element.deleted,
            }
        else:
            result = {
                'openstreetmap_id': openstreetmap_element.openstreetmap_id,
                'type': openstreetmap_element.type,
                'latitude': openstreetmap_element.latitude,
                'longitude': openstreetmap_element.longitude,
            }
        
            if not self.restrict_fields:
                result.update({
                    'url': u'https://www.openstreetmap.org/{type}/{id}'.format(type=openstreetmap_element.type, id=encoding.escape_uri_path(openstreetmap_element.openstreetmap_id)),
                    'name': openstreetmap_element.name,
                    'sorting_name': openstreetmap_element.sorting_name,
                    'nature': openstreetmap_element.nature,
                    'wikidata': openstreetmap_element.wikidata.split(';'),
                    'wikimedia_commons': openstreetmap_element.wikimedia_commons,
                })
        
        return result
    
    def wikidata_entry_dict(self, wikidata_entry):
        if wikidata_entry.deleted:
            result = {
                'wikidata_id': wikidata_entry.wikidata_id,
                'deleted': wikidata_entry.deleted,
            }
        else:
            result = {
                'wikidata_id': wikidata_entry.wikidata_id,
            }
        
            if 'Q5' in wikidata_entry.instance_of.split(';'):
                result.update({
                    'date_of_birth': wikidata_entry.date_of_birth,
                    'date_of_birth_accuracy': wikidata_entry.date_of_birth_accuracy,
                    'date_of_death': wikidata_entry.date_of_death,
                    'date_of_death_accuracy': wikidata_entry.date_of_death_accuracy,
                })
        
            if not self.restrict_fields:
                result.update({
                    'url': u'https://www.wikidata.org/wiki/{name}'.format(name=encoding.escape_uri_path(wikidata_entry.wikidata_id)),
                    'instance_of': wikidata_entry.instance_of.split(';'),
                    'burial_plot_reference': wikidata_entry.burial_plot_reference,
                    'wikimedia_commons_category': wikidata_entry.wikimedia_commons_category,
                })
            
                if 'Q5' in wikidata_entry.instance_of.split(';'):
                    result.update({
                        'sex_or_gender': wikidata_entry.sex_or_gender,
                        'occupations': wikidata_entry.occupations.split(';'),
                        'wikimedia_commons_grave_category': wikidata_entry.wikimedia_commons_grave_category,
                    })
                else:
                    result.update({
                        'grave_of': wikidata_entry.grave_of_wikidata.split(';'),
                    })
        
            localizations = []
            if self.languages:
                for language in self.languages:
                    wikidata_localized_entry = wikidata_entry.localizations.filter(language=language).first()
                    if wikidata_localized_entry:
                        localizations.append({
                            'id': wikidata_localized_entry.pk,
                            'language_code': language.code,
                            'name': wikidata_localized_entry.wikipedia,
                            'description': wikidata_localized_entry.description,
                            'wikipedia': self.wikipedia_page_dict(wikidata_localized_entry),
                        })
            result['localizations'] = localizations
        
        return result
    
    def wikipedia_page_dict(self, wikidata_localized_entry):
        wikipedia_page = WikipediaPage.objects.filter(wikidata_localized_entry=wikidata_localized_entry).first()
        if wikipedia_page:
            result = {
                'id': wikipedia_page.pk,
                'title': wikipedia_page.title,
                'intro': wikipedia_page.intro,
            }
            
            if not self.restrict_fields:
                result.update({
                    'default_sort': wikipedia_page.default_sort,
                    'url': u'https://{language}.wikipedia.org/wiki/{name}'.format(language=wikidata_localized_entry.language.code, name=encoding.escape_uri_path(wikidata_localized_entry.wikipedia)),
                })
        else:
            result = None
        
        return result
    
    def wikimedia_commons_category_dict(self, wikimedia_commons_category):
        
        if wikimedia_commons_category:
            if wikimedia_commons_category.deleted:
                result = {
                    'wikimedia_commons_id': wikimedia_commons_category.wikimedia_commons_id,
                    'deleted': wikimedia_commons_category.deleted,
                }
            else:
                result = {
                    'wikimedia_commons_id': wikimedia_commons_category.wikimedia_commons_id,
                    'main_image': wikimedia_commons_category.main_image,
                    'category_members': wikimedia_commons_category.category_members_list(),
                }
        
                if not self.restrict_fields:
                    result.update({
                        'url': u'https://commons.wikimedia.org/wiki/{name}'.format(name=encoding.escape_uri_path(wikimedia_commons_category.wikimedia_commons_id)),
                        'url_main_image': u'https://commons.wikimedia.org/wiki/{name}'.format(name=encoding.escape_uri_path(wikimedia_commons_category.main_image)),
                    })
        else:
            result = None
        
        return result

def get_languages(request):
    language_code = request.GET.get('language', None)
    if language_code:
        languages = Language.objects.filter(code=language_code)
    else:
        languages = Language.objects.all()

    return languages

def get_modified_since(request):
    try:
        modified_since = request.GET.get('modified_since', None)
        if modified_since:
            # Parse date
            modified_since = dateparse.parse_date(modified_since)
            
            # Convert to datetime with 00:00 for server time zone
            modified_since = datetime.datetime.combine(modified_since, datetime.time()).replace(tzinfo=timezone.get_current_timezone())
    
        return modified_since
    except:
        raise SuspiciousOperation('Invalid parameter : modified_since')

def get_restrict_fields(request, default=False):
    restrict_fields = request.GET.get('restrict_fields', default)
    
    if restrict_fields == 'False' or restrict_fields == 'false' or restrict_fields == '0' or restrict_fields == 0:
        restrict_fields = False
    elif restrict_fields or restrict_fields == '':
        restrict_fields = True
    else:
        restrict_fields = default
    
    return restrict_fields

def get_related_objects(request, default=False):
    related_objects = request.GET.get('related_objects', default)
    
    if related_objects == 'False' or related_objects == 'false' or related_objects == '0' or related_objects == 0:
        related_objects = False
    elif related_objects or related_objects == '':
        related_objects = True
    else:
        related_objects = default
    
    return related_objects

def get_search(request):
    search = request.GET.get('search', u'')
    
    return search

def get_categories(request):
    categories = request.GET.getlist('category', [])
    
    return categories

def get_sector(request):
    sector = request.GET.get('sector', u'')
    
    return sector

def get_born_after(request):
    try:
        born_after = request.GET.get('born_after', None)
        if born_after:
            # Parse date
            born_after = datetime.date(int(born_after), 1, 1)
            
            # Convert to datetime with 00:00 for server time zone
            born_after = datetime.datetime.combine(born_after, datetime.time()).replace(tzinfo=timezone.get_current_timezone()).date()
    
        return born_after
    except:
        raise SuspiciousOperation('Invalid parameter : born_after')

def get_died_before(request):
    try:
        died_before = request.GET.get('died_before', None)
        if died_before:
            # Parse date
            died_before = datetime.date(int(died_before), 12, 31)
            
            # Convert to datetime with 00:00 for server time zone
            died_before = datetime.datetime.combine(died_before, datetime.time()).replace(tzinfo=timezone.get_current_timezone()).date()
    
        return died_before
    except:
        raise SuspiciousOperation('Invalid parameter : died_before')

@require_http_methods(["GET"])
def licence(request):
    content = [request.build_absolute_uri(reverse(licence)) + '\n']
    
    with open(os.path.dirname(__file__) + '/LICENSE_DATABASE.txt', 'r') as content_file:
        content.append(content_file.read())
    
    return HttpResponse('\n'.join(content), content_type='text/plain; charset=utf-8')

@require_http_methods(["GET"])
def openstreetmap_element_list(request, type=None):
    restrict_fields = get_restrict_fields(request)
    modified_since = get_modified_since(request)
    search = get_search(request)
    
    if modified_since:
        openstreetmap_elements = OpenStreetMapElement.objects.filter(modified__gt=modified_since)
    else:
        openstreetmap_elements = OpenStreetMapElement.objects.filter(deleted=False)
    
    if type:
        openstreetmap_elements = openstreetmap_elements.filter(type=type)
    
    for search_term in search.split():
        openstreetmap_elements = openstreetmap_elements.filter( \
            Q(name__icontains=search_term) \
        )
    
    openstreetmap_elements = openstreetmap_elements.order_by('sorting_name').distinct('sorting_name')
    
    paginator = Paginator(openstreetmap_elements, 25)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_content = paginator.page(paginator.num_pages)
    
    obj_to_encode = {
        'openstreetmap_elements': page_content.object_list,
        'page': page_content,
    }
    
    content = SuperLachaiseEncoder(request, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def openstreetmap_element(request, type, id):
    restrict_fields = get_restrict_fields(request)
    
    try:
        openstreetmap_element = OpenStreetMapElement.objects.get(type=type, openstreetmap_id=id, deleted=False)
    except OpenStreetMapElement.DoesNotExist:
        raise Http404(_('OpenStreetMap element does not exist'))
    
    content = SuperLachaiseEncoder(request, restrict_fields=restrict_fields).encode({'openstreetmap_element': openstreetmap_element})
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def wikidata_entry_list(request):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    modified_since = get_modified_since(request)
    search = get_search(request)
    
    if modified_since:
        wikidata_entries = WikidataEntry.objects.filter(modified__gt=modified_since)
    else:
        wikidata_entries = WikidataEntry.objects.filter(deleted=False)
    
    for search_term in search.split():
        wikidata_entries = wikidata_entries.filter( \
            Q(localizations__name__icontains=search_term) \
            | Q(localizations__description__icontains=search_term) \
            | Q(localizations__wikipedia__icontains=search_term) \
        )
    
    wikidata_entries = wikidata_entries.order_by('id').distinct('id')
    
    paginator = Paginator(wikidata_entries, 25)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_content = paginator.page(paginator.num_pages)
    
    obj_to_encode = {
        'wikidata_entries': page_content.object_list,
        'page': page_content,
    }
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def wikidata_entry(request, id):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    
    try:
        wikidata_entry = WikidataEntry.objects.get(wikidata_id=id, deleted=False)
    except WikidataEntry.DoesNotExist:
        raise Http404(_('Wikidata entry does not exist'))
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode({'wikidata_entry': wikidata_entry})
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def wikimedia_commons_category_list(request):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    modified_since = get_modified_since(request)
    search = get_search(request)
    
    if modified_since:
        wikimedia_commons_categories = WikimediaCommonsCategory.objects.filter(modified__gt=modified_since)
    else:
        wikimedia_commons_categories = WikimediaCommonsCategory.objects.filter(deleted=False)
    
    for search_term in search.split():
        wikimedia_commons_categories = wikimedia_commons_categories.filter( \
            Q(id__icontains=search_term) \
            | Q(main_image__icontains=search_term) \
        )
    
    wikimedia_commons_categories = wikimedia_commons_categories.order_by('id').distinct('id')
    
    paginator = Paginator(wikimedia_commons_categories, 25)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_content = paginator.page(paginator.num_pages)
    
    obj_to_encode = {
        'wikimedia_commons_categories': page_content.object_list,
        'page': page_content,
    }
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def wikimedia_commons_category(request, id):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    
    try:
        wikimedia_commons_category = WikimediaCommonsCategory.objects.get(wikimedia_commons_id=id, deleted=False)
    except WikimediaCommonsCategory.DoesNotExist:
        raise Http404(_('Wikimedia Commons category does not exist'))
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode({'wikimedia_commons_category': wikimedia_commons_category})
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def superlachaise_category_list(request):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    modified_since = get_modified_since(request)
    search = get_search(request)
    
    if modified_since:
        superlachaise_categories = SuperLachaiseCategory.objects.filter(modified__gt=modified_since)
    else:
        superlachaise_categories = SuperLachaiseCategory.objects.filter(deleted=False)
    
    for search_term in search.split():
        superlachaise_categories = superlachaise_categories.filter( \
            Q(code__icontains=search_term) \
            | Q(type__icontains=search_term) \
            | Q(values__icontains=search_term) \
            | Q(localizations__name__icontains=search_term) \
        )
    
    superlachaise_categories = superlachaise_categories.order_by('code').distinct('code')
    
    paginator = Paginator(superlachaise_categories, 25)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_content = paginator.page(paginator.num_pages)
    
    obj_to_encode = {
        'superlachaise_categories': page_content.object_list,
        'page': page_content,
    }
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def superlachaise_category(request, id):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    
    try:
        superlachaise_category = SuperLachaiseCategory.objects.get(code=id, deleted=False)
    except SuperLachaiseCategory.DoesNotExist:
        raise Http404(_('SuperLachaise category does not exist'))
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode({'superlachaise_category': superlachaise_category})
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def superlachaise_poi_list(request):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    modified_since = get_modified_since(request)
    search = get_search(request)
    categories = get_categories(request)
    sector = get_sector(request)
    born_after = get_born_after(request)
    died_before = get_died_before(request)
    related_objects = get_related_objects(request, False)
    
    if modified_since:
        superlachaise_pois = SuperLachaisePOI.objects.filter(modified__gt=modified_since)
    else:
        superlachaise_pois = SuperLachaisePOI.objects.filter(deleted=False)
    
    for search_term in search.split():
        superlachaise_pois = superlachaise_pois.filter( \
            Q(localizations__name__icontains=search_term) \
            | Q(localizations__description__icontains=search_term) \
            | Q(wikidata_entries__localizations__name__icontains=search_term) \
            | Q(wikidata_entries__localizations__description__icontains=search_term) \
            | Q(wikidata_entries__localizations__wikipedia__icontains=search_term) \
        )
    
    # Apply AND to multiple 'category' keys in query ex. 'category=cinema&category=women'
    for category in categories:
        # Apply OR to multiple categories in value ex. 'category=cinema+theatre'
        superlachaise_pois = superlachaise_pois.filter(superlachaise_categories__code__in=category.split())
    
    if sector:
        superlachaise_pois = superlachaise_pois.filter(wikidata_entries__burial_plot_reference__in=sector.split())
    
    if born_after:
        superlachaise_pois = superlachaise_pois.filter(wikidata_entries__date_of_birth__gte=born_after)
    if died_before:
        superlachaise_pois = superlachaise_pois.filter(wikidata_entries__date_of_death__lte=died_before)
    
    superlachaise_pois = superlachaise_pois.order_by('openstreetmap_element_id').distinct('openstreetmap_element_id')
    
    paginator = Paginator(superlachaise_pois, 25)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_content = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_content = paginator.page(paginator.num_pages)
    
    wikidata_entries = superlachaise_categories = []
    if page_content.object_list:
        wikidata_entries = WikidataEntry.objects.filter(superlachaisewikidatarelation__superlachaise_poi__in=page_content.object_list).distinct()
        superlachaise_categories = SuperLachaiseCategory.objects.filter(superlachaisecategoryrelation__superlachaise_poi__in=page_content.object_list).distinct()
    
    obj_to_encode = {
        'superlachaise_pois': page_content.object_list,
        'page': page_content,
    }
    
    if related_objects:
        if page_content.object_list:
            openstreetmap_elements = [superlachaise_poi.openstreetmap_element for superlachaise_poi in page_content.object_list if superlachaise_poi.openstreetmap_element]
            wikimedia_commons_categories = [superlachaise_poi.wikimedia_commons_category for superlachaise_poi in page_content.object_list if superlachaise_poi.wikimedia_commons_category]
            wikidata_entries = WikidataEntry.objects.filter(superlachaisewikidatarelation__superlachaise_poi__in=page_content.object_list).distinct()
            superlachaise_categories = SuperLachaiseCategory.objects.filter(superlachaisecategoryrelation__superlachaise_poi__in=page_content.object_list).distinct()
            obj_to_encode['related_objects'] = {
                'openstreetmap_elements': openstreetmap_elements,
                'wikimedia_commons_categories': wikimedia_commons_categories,
                'wikidata_entries': wikidata_entries,
                'superlachaise_categories': superlachaise_categories,
            }
        else:
            obj_to_encode['related_objects'] = None
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def superlachaise_poi(request, id):
    languages = get_languages(request)
    restrict_fields = get_restrict_fields(request)
    related_objects = get_related_objects(request, False)
    
    try:
        superlachaise_poi = SuperLachaisePOI.objects.get(pk=id, deleted=False)
    except SuperLachaisePOI.DoesNotExist:
        raise Http404(_('SuperLachaise POI does not exist'))
    
    obj_to_encode = {
        'superlachaise_poi': superlachaise_poi,
    }
    
    if related_objects:
        obj_to_encode['related_objects'] = {
            'openstreetmap_element': superlachaise_poi.openstreetmap_element if superlachaise_poi.openstreetmap_element else None,
            'wikimedia_commons_category': superlachaise_poi.wikimedia_commons_category if superlachaise_poi.wikimedia_commons_category else None,
            'wikidata_entries': superlachaise_poi.wikidata_entries.all(),
            'superlachaise_categories': superlachaise_poi.superlachaise_categories.all(),
        }
    
    content = SuperLachaiseEncoder(request, languages=languages, restrict_fields=restrict_fields).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def objects(request):
    modified_since = get_modified_since(request)
    
    objects = {}
    
    for model, view in [
        (OpenStreetMapElement, openstreetmap_element_list),
        (WikidataEntry, wikidata_entry_list),
        (WikimediaCommonsCategory, wikimedia_commons_category_list),
        (SuperLachaiseCategory, superlachaise_category_list),
        (SuperLachaisePOI, superlachaise_poi_list),
    ]:
        if modified_since:
            count = model.objects.filter(modified__gt=modified_since).count()
        else:
            count = model.objects.filter(deleted=False).count()
        
        if request.GET:
            path = '?'.join([reverse(view), '&'.join('%s=%s' % (key, value) for key, value in request.GET.iteritems())])
        else:
            path = reverse(view)
        
        objects[model.__name__] = {
            'count': count,
            'url': request.build_absolute_uri(path.replace(' ', '+')),
        }
    
    obj_to_encode = {
        'objects': objects,
    }
    
    content = SuperLachaiseEncoder(request).encode(obj_to_encode)
    
    return HttpResponse(content, content_type='application/json; charset=utf-8')
