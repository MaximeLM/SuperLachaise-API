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

import datetime, dateutil.parser, json
from decimal import Decimal
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from superlachaise_api.models import *

def to_json_string(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        return obj

def dump_json(jsonObject):
    return json.dumps(jsonObject, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, default=to_json_string)

def get_superlachaise_pois_dict(superlachaise_pois, languages):
    result = []
    
    for superlachaise_poi in superlachaise_pois:
        result.append(get_superlachaise_poi_dict(superlachaise_poi, languages))
    
    return {'superlachaise_pois': result}

def get_superlachaise_poi_dict(superlachaise_poi, languages):
    result = {
        'openstreetmap_element': get_openstreetmap_element_dict(superlachaise_poi.openstreetmap_element),
        'wikimedia_commons_category': get_wikimedia_commons_category_dict(superlachaise_poi.wikimedia_commons_category, superlachaise_poi.main_image),
    }
    
    for language in languages:
        superlachaise_localized_poi = superlachaise_poi.localizations.filter(language=language).first()
        if superlachaise_localized_poi:
            result[language.code] = {
                'name': superlachaise_localized_poi.name,
                'description': superlachaise_localized_poi.description,
            }
    
    wikidata_entries = {}
    for wikidata_entry_relation in superlachaise_poi.superlachaisewikidatarelation_set.all():
        if not wikidata_entry_relation.relation_type in wikidata_entries:
            wikidata_entries[wikidata_entry_relation.relation_type] = []
        wikidata_entries[wikidata_entry_relation.relation_type].append(get_wikidata_entry_dict(wikidata_entry_relation.wikidata_entry, languages))
    result['wikidata_entries'] = wikidata_entries
    
    categories = []
    for category in superlachaise_poi.categories.all():
        categories.append(get_category_dict(category, languages))
    result['categories'] = categories
    
    return result

def get_openstreetmap_element_dict(openstreetmap_element):
    result = {
        'id': openstreetmap_element.id,
        'sorting_name': openstreetmap_element.sorting_name,
        'latitude': openstreetmap_element.latitude,
        'longitude': openstreetmap_element.longitude,
    }
    
    return result

def get_wikidata_entry_dict(wikidata_entry, languages):
    result = {
        'id': wikidata_entry.id,
    }
    
    if wikidata_entry.date_of_birth:
        result['date_of_birth'] = wikidata_entry.date_of_birth
    if wikidata_entry.date_of_birth_accuracy:
        result['date_of_birth_accuracy'] = wikidata_entry.date_of_birth_accuracy
    if wikidata_entry.date_of_death:
        result['date_of_death'] = wikidata_entry.date_of_death
    if wikidata_entry.date_of_death_accuracy:
        result['date_of_death_accuracy'] = wikidata_entry.date_of_death_accuracy
    if wikidata_entry.burial_plot_reference:
        result['burial_plot_reference'] = wikidata_entry.burial_plot_reference
    
    for language in languages:
        wikidata_localized_entry = wikidata_entry.localizations.filter(language=language).first()
        if wikidata_localized_entry:
            result[language.code] = {
                'name': wikidata_localized_entry.name,
                'intro': wikidata_localized_entry.intro,
            }
    
    return result

def get_wikimedia_commons_category_dict(wikimedia_commons_category, main_image):
    result = None
    
    if wikimedia_commons_category:
        result = {
            'name': 'Category:' + wikimedia_commons_category.id,
            'files': wikimedia_commons_category.files,
            'main_image': main_image.id if main_image else None,
        }
    
    return result

def get_category_dict(category, languages):
    result = {
        'code': category.code,
        'type': category.type,
    }
    
    for language in languages:
        localized_category = category.localizations.filter(language=language).first()
        if localized_category:
            result[language.code] = {
                'name': localized_category.name,
            }
    
    return result

def get_languages(request):
    language_code = request.GET.get('lang', None)
    if language_code:
        languages = Language.objects.filter(code=language_code)
    else:
        languages = Language.objects.all()
    
    return languages

@require_http_methods(["GET"])
def superlachaise_poi_list(request):
    modified_since = request.GET.get('modified_since', None)
    print dateutil.parser.parse(modified_since)
    # Get objects
    if modified_since:
        superlachaise_pois = SuperLachaisePOI.objects.filter(modified__gt=dateutil.parser.parse(modified_since))
    else:
        superlachaise_pois = SuperLachaisePOI.objects.all()
    
    # Prepare dict
    result = get_superlachaise_pois_dict(superlachaise_pois, get_languages(request))
    
    content = dump_json(result)
    return HttpResponse(content, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def superlachaise_poi(request, id):
    # Get objects
    superlachaise_pois = [SuperLachaisePOI.objects.get(openstreetmap_element__id=id)]
    
    # Prepare dict
    result = get_superlachaise_pois_dict(superlachaise_pois, get_languages(request))
    
    content = dump_json(result)
    return HttpResponse(content, content_type='application/json; charset=utf-8')
