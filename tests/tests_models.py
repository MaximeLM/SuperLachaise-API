# -*- coding: utf-8 -*-

"""
tests_models.py
superlachaise_api

Created by Maxime Le Moine on 15/06/2015.
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

from decimal import Decimal
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.test import TestCase
from django.utils import timezone

from superlachaise_api.models import *

class OpenStreetMapElementTestCase(TestCase):
    
    def test_openstreetmap_url_returns_none_if_type_is_empty(self):
        openstreetmap_id = "123456"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        
        self.assertIsNone(openstreetmap_element.openstreetmap_url())
    
    def test_openstreetmap_url_returns_openstreetmap_url_with_type_and_id_if_type_is_not_empty(self):
        openstreetmap_id = "123456"
        type = "node"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, type=type)
        
        self.assertEqual(OpenStreetMapElement.URL_FORMAT.format(type=type, id=openstreetmap_id), openstreetmap_element.openstreetmap_url())
    
    def test_wikidata_list_returns_none_if_wikidata_is_empty(self):
        openstreetmap_id = "123456"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        
        self.assertIsNone(openstreetmap_element.wikidata_list())
    
    def test_wikidata_list_returns_wikidata_if_wikidata_has_no_semicolon(self):
        openstreetmap_id = "123456"
        wikidata = "Q123456"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, wikidata=wikidata)
        
        self.assertEqual([wikidata], openstreetmap_element.wikidata_list())
    
    def test_wikidata_list_returns_wikidata_splitted_by_semicolon_if_wikidata_has_semicolon(self):
        openstreetmap_id = "123456"
        wikidata_1 = "Q456"
        wikidata_2 = "Q123"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, wikidata=';'.join([wikidata_1, wikidata_2]))
        
        self.assertEqual([wikidata_1, wikidata_2], openstreetmap_element.wikidata_list())
    
    def test_wikidata_url_returns_wikidata_url_with_language_and_wikidata_if_wikidata_has_no_colon(self):
        language_code = "en"
        openstreetmap_id = "123456"
        wikidata = "Q123"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, wikidata=wikidata)
        
        self.assertEqual(WikidataEntry.URL_FORMAT.format(id=wikidata, language_code=language_code), openstreetmap_element.wikidata_url(language_code, wikidata))
    
    def test_wikidata_url_returns_wikidata_url_with_language_and_last_part_of_wikidata_splitted_by_colon_if_wikidata_has_colon(self):
        language_code = "en"
        openstreetmap_id = "123456"
        prefix = "artist"
        suffix = "Q123"
        wikidata = ':'.join([prefix, suffix])
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, wikidata=wikidata)
        
        self.assertEqual(WikidataEntry.URL_FORMAT.format(id=suffix, language_code=language_code), openstreetmap_element.wikidata_url(language_code, wikidata))
    
    def test_wikimedia_commons_url_returns_none_if_wikimedia_commons_is_empty(self):
        openstreetmap_id = "123456"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        
        self.assertIsNone(openstreetmap_element.wikimedia_commons_url())
    
    def test_wikimedia_commons_url_returns_wikimedia_commons_url_with_wikimedia_commons_if_wikimedia_commons_is_not_empty(self):
        openstreetmap_id = "123456"
        wikimedia_commons = "wikimedia commons"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, wikimedia_commons=wikimedia_commons)
        
        self.assertEqual(WikimediaCommonsCategory.URL_FORMAT.format(title=wikimedia_commons), openstreetmap_element.wikimedia_commons_url())

class WikidataEntryTestCase(TestCase):
    
    def test_wikidata_list_returns_none_if_field_value_is_empty(self):
        wikidata_id = "wikidata_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        
        self.assertIsNone(wikidata_entry.wikidata_list("occupations"))
    
    def test_wikidata_list_returns_field_value_splitted_by_semicolon_if_field_value_is_not_empty(self):
        wikidata_id = "wikidata_id"
        occupation_1 = "occupation_1"
        occupation_2 = "occupation_2"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id, occupations=';'.join([occupation_1, occupation_2]))
        
        self.assertEqual([occupation_1, occupation_2], wikidata_entry.wikidata_list("occupations"))
    
    def test_wikidata_url_returns_wikidata_url_with_language_and_field_value_if_field_value_is_not_empty(self):
        language_code = "en"
        wikidata_id = "Q123"
        occupations = "occupations"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id, occupations=occupations)
        
        self.assertEqual(WikidataEntry.URL_FORMAT.format(id=occupations, language_code=language_code), wikidata_entry.wikidata_url(language_code, occupations))
    
    def test_wikimedia_commons_category_url_returns_none_if_field_value_is_empty(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        
        self.assertIsNone(wikidata_entry.wikimedia_commons_category_url("wikimedia_commons_category"))
    
    def test_wikimedia_commons_category_url_returns_wikimedia_commons_url_with_category_and_field_value_if_field_value_is_not_empty(self):
        wikimedia_commons_category = "wikimedia_commons_category"
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id", wikimedia_commons_category=wikimedia_commons_category)
        
        self.assertEqual(WikimediaCommonsCategory.URL_FORMAT.format(title=u'Category:%s' % wikimedia_commons_category), wikidata_entry.wikimedia_commons_category_url("wikimedia_commons_category"))

class WikidataLocalizedEntryTestCase(TestCase):
    
    def test_save_updates_wikidata_entry_modified(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        now = timezone.now()
        
        WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language).save()
        
        self.assertTrue(wikidata_entry.modified > now)
    
    def test_delete_updates_wikidata_entry_modified(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry.objects.create(wikidata_entry=wikidata_entry, language=language)
        now = timezone.now()
        
        wikidata_localized_entry.delete()
        
        self.assertTrue(wikidata_entry.modified > now)
    
    def test_wikipedia_url_returns_none_if_wikipedia_is_empty(self):
        wikidata_id = "wikidata_id"
        language_code = "language_code"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        
        self.assertIsNone(wikidata_localized_entry.wikipedia_url())
    
    def test_wikipedia_url_returns_wikipedia_url_with_language_and_wikipedia_if_wikipedia_is_not_empty(self):
        wikidata_id = "wikidata_id"
        language_code = "language_code"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikipedia = "wikipedia"
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language, wikipedia=wikipedia)
        
        self.assertEqual(WikipediaPage.URL_FORMAT.format(language_code=language.code, title=wikipedia), wikidata_localized_entry.wikipedia_url())
    
    def test_sorting_name_returns_name_if_wikipedia_page_is_none(self):
        wikidata_id = "wikidata_id"
        language_code = "language_code"
        name = "name"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language, name=name)
        
        self.assertEqual(name, wikidata_localized_entry.sorting_name())
    
    def test_sorting_name_returns_name_if_wikipedia_page_default_sort_is_blank(self):
        wikidata_id = "wikidata_id"
        language_code = "language_code"
        name = "name"
        default_sort = ""
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language, name=name)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage(wikidata_localized_entry=wikidata_localized_entry, default_sort=default_sort)
        wikipedia_page.save()
        
        self.assertEqual(name, wikidata_localized_entry.sorting_name())
    
    def test_sorting_name_returns_default_sort_if_wikipedia_page_default_sort_is_not_blank(self):
        wikidata_id = "wikidata_id"
        language_code = "language_code"
        name = "name"
        default_sort = "default_sort"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language, name=name)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage(wikidata_localized_entry=wikidata_localized_entry, default_sort=default_sort)
        wikipedia_page.save()
        
        self.assertEqual(default_sort, wikidata_localized_entry.sorting_name())

class WikipediaPageTestCase(TestCase):
    
    def test_save_updates_wikidata_localized_entry_modified(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        now = timezone.now()
        
        WikipediaPage(wikidata_localized_entry=wikidata_localized_entry).save()
        
        self.assertTrue(wikidata_localized_entry.modified > now)
    
    def test_delete_updates_wikidata_localized_entry_modified(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage.objects.create(wikidata_localized_entry=wikidata_localized_entry)
        now = timezone.now()
        
        wikipedia_page.delete()
        
        self.assertTrue(wikidata_localized_entry.modified > now)
    
    def test_full_clean_deletes_carriage_returns_in_intro(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage(wikidata_localized_entry=wikidata_localized_entry, intro="intro\r\nnext\n", title="title")
        
        wikipedia_page.full_clean()
        
        self.assertFalse('\r' in wikipedia_page.intro)

class WikimediaCommonsCategoryTestCase(TestCase):
    
    def test_category_members_list_returns_empty_list_if_field_value_is_empty(self):
        wikimedia_commons_id = "some_wikimedia_commons_id"
        wikimedia_commons_category = WikimediaCommonsCategory(wikimedia_commons_id=wikimedia_commons_id)
        
        self.assertEqual([], wikimedia_commons_category.category_members_list())
    
    def test_category_members_list_returns_field_value_splitted_by_pipe_if_field_value_is_not_empty(self):
        wikimedia_commons_id = "some_wikimedia_commons_id"
        member_1 = "some_member_1"
        member_2 = "some_member_2"
        wikimedia_commons_category = WikimediaCommonsCategory(wikimedia_commons_id=wikimedia_commons_id, category_members='|'.join([member_1, member_2]))
        
        self.assertEqual([member_1, member_2], wikimedia_commons_category.category_members_list())
    
    def test_wikimedia_commons_url_returns_none_if_field_value_is_empty(self):
        wikimedia_commons_category = WikimediaCommonsCategory(wikimedia_commons_id="wikimedia_commons_id")
        
        self.assertIsNone(wikimedia_commons_category.wikimedia_commons_url(""))
    
    def test_wikimedia_commons_url_returns_wikimedia_commons_url_with_field_value_if_field_value_is_not_empty(self):
        main_image = "image"
        wikimedia_commons_category = WikimediaCommonsCategory(wikimedia_commons_id="wikimedia_commons_id", main_image=main_image)
        
        self.assertEqual(WikimediaCommonsCategory.URL_FORMAT.format(title=main_image), wikimedia_commons_category.wikimedia_commons_url(main_image))

class WikimediaCommonsFileTestCase(TestCase):
    
    def test_wikimedia_commons_url_returns_wikimedia_commons_url_with_id(self):
        wikimedia_commons_id = "id"
        wikimedia_commons_file = WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id)
        
        self.assertEqual(WikimediaCommonsCategory.URL_FORMAT.format(title=wikimedia_commons_id), wikimedia_commons_file.wikimedia_commons_url())

class SuperLachaiseLocalizedPOITestCase(TestCase):
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        language = Language(code="code")
        language.save()
        now = timezone.now()
        
        SuperLachaiseLocalizedPOI(superlachaise_poi=superlachaise_poi, language=language).save()
        
        self.assertTrue(superlachaise_poi.modified > now)
    
    def test_delete_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        language = Language(code="code")
        language.save()
        superlachaise_localized_poi = SuperLachaiseLocalizedPOI.objects.create(superlachaise_poi=superlachaise_poi, language=language)
        now = timezone.now()
        
        superlachaise_localized_poi.delete()
        
        self.assertTrue(superlachaise_poi.modified > now)

class SuperLachaiseWikidataRelationTestCase(TestCase):
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        relation_type = "relation_type"
        now = timezone.now()
        
        SuperLachaiseWikidataRelation(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type).save()
        
        self.assertTrue(superlachaise_poi.modified > now)
    
    def test_delete_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        relation_type = "relation_type"
        superlachaise_wikidata_relation = SuperLachaiseWikidataRelation.objects.create(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type)
        now = timezone.now()
        
        superlachaise_wikidata_relation.delete()
        
        self.assertTrue(superlachaise_poi.modified > now)

class SuperLachaiseLocalizedCategoryTestCase(TestCase):
    
    def test_save_updates_superlachaise_category_modified(self):
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        language = Language(code="code")
        language.save()
        superlachaise_category.save()
        now = timezone.now()
        
        SuperLachaiseLocalizedCategory(superlachaise_category=superlachaise_category, language=language).save()
        
        self.assertTrue(superlachaise_category.modified > now)
    
    def test_delete_updates_superlachaise_category_modified(self):
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        language = Language(code="code")
        language.save()
        superlachaise_category.save()
        superlachaise_localized_category = SuperLachaiseLocalizedCategory.objects.create(superlachaise_category=superlachaise_category, language=language)
        now = timezone.now()
        
        superlachaise_localized_category.delete()
        
        self.assertTrue(superlachaise_category.modified > now)

class SuperLachaiseCategoryRelationTestCase(TestCase):
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        now = timezone.now()
        
        SuperLachaiseCategoryRelation(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category).save()
        
        self.assertTrue(superlachaise_poi.modified > now)
    
    def test_delete_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        superlachaise_category_relation = SuperLachaiseCategoryRelation.objects.create(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category)
        now = timezone.now()
        
        superlachaise_category_relation.delete()
        
        self.assertTrue(superlachaise_poi.modified > now)

class WikidataOccupationTestCase(TestCase):
    
    def test_wikidata_url_returns_wikidata_url_with_wikidata_id(self):
        language_code = "en"
        wikidata_id = "Q123"
        wikidata_occupation = WikidataOccupation(wikidata_id=wikidata_id)
        
        self.assertEqual(WikidataEntry.URL_FORMAT.format(id=wikidata_id, language_code=language_code), wikidata_occupation.wikidata_url(language_code))
