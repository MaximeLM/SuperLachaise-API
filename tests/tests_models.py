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

class PendingModificationTestCase(TestCase):
    
    def test_validation_fails_if_target_object_id_is_not_json(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = "target_object_id"
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_target_object_id_is_not_json_dict(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '["target_object_id"]'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_target_object_id_has_field_not_in_target_object_model_fields(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"field":"value"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_succeeds_if_target_object_id_has_field_following_target_object_model_relation(self):
        target_object_class = "WikidataLocalizedEntry"
        target_object_id = '{"wikidata_entry__wikidata_id":"wikidata_id", "language__code":"fr"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        
        try:
            pending_modification.full_clean()
        except ValidationError:
            self.fail()
    
    def test_validation_succeeds_if_target_object_id_has_field_following_target_object_model_one_to_one_relation(self):
        target_object_class = "SuperLachaisePOI"
        target_object_id = '{"openstreetmap_element__openstreetmap_id":"openstreetmap_id", "openstreetmap_element__type":"type"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        
        try:
            pending_modification.full_clean()
        except ValidationError:
            self.fail()
    
    def test_validation_fails_if_modified_fields_is_not_json(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = 'modified_fields'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_is_not_json_dict(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = '["modified_fields"]'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_has_field_not_in_target_object_model_fields(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = '{"field":"value"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_succeeds_if_modified_fields_has_field_following_target_object_model_relation(self):
        target_object_class = "WikidataOccupation"
        target_object_id = '{"wikidata_id":"wikidata_id"}'
        modified_fields = '{"superlachaise_category__code":"code"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
        except ValidationError:
            self.fail()
    
    def test_validation_succeeds_if_modified_fields_has_field_following_target_object_model_one_to_one_relation(self):
        target_object_class = "SuperLachaisePOI"
        target_object_id = '{"openstreetmap_element__openstreetmap_id":"openstreetmap_id", "openstreetmap_element__type":"type"}'
        modified_fields = '{"openstreetmap_element__openstreetmap_id":"openstreetmap_id", "openstreetmap_element__type":"type"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
        except ValidationError:
            self.fail()
    
    def test_validation_fails_if_modified_fields_has_id_field(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = '{"id:5"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_has_pk_field(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = '{"pk:5"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_target_object_model_returns_model_if_model_exists(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = "target_object_id"
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertEqual(OpenStreetMapElement, pending_modification.target_object_model())
    
    def test_target_object_model_raises_lookup_error_if_model_does_not_exist(self):
        target_object_class = "target_object_class"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        try:
            pending_modification.target_object_model()
            self.fail()
        except LookupError:
            pass
    
    def test_target_object_returns_target_object_if_target_object_exists(self):
        language_code = "language_code"
        language = Language(code=language_code)
        language.save()
        wikidata_entry_id = "wikidata_entry_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        target_object_class = "WikidataLocalizedEntry"
        target_object_id = '{"wikidata_entry__wikidata_id":"%s", "language__code":"%s"}' % (wikidata_entry_id, language_code)
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertEqual(wikidata_localized_entry.pk, pending_modification.target_object().pk)
    
    def test_target_object_returns_none_if_target_object_class_is_not_valid(self):
        target_object_class = "target_object_class"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertIsNone(pending_modification.target_object())
    
    def test_target_object_returns_none_if_target_object_id_is_not_valid(self):
        target_object_class = "OpenStreetMap"
        target_object_id = 'target_object_id'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertIsNone(pending_modification.target_object())
    
    def test_target_object_returns_none_if_target_object_does_not_exist(self):
        language_code = "language_code"
        wikidata_entry_id = "wikidata_entry_id"
        language_code = "language_code"
        language = Language(code=language_code)
        language.save()
        wikidata_entry_id = "wikidata_entry_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        target_object_class = "WikidataLocalizedEntry"
        target_object_id = '{"wikidata_entry__wikidata_id":"%s", "language__code":"%s"}' % (wikidata_entry_id, language_code)
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertIsNone(pending_modification.target_object())
    
    def test_resolve_field_relation_returns_field_and_value_if_field_is_simple(self):
        object_model = OpenStreetMapElement
        field = 'name'
        value = 'value'
        
        self.assertEqual((field, value), PendingModification.resolve_field_relation(object_model, field, value))
    
    def test_resolve_field_relation_raises_does_not_exist_if_field_is_not_in_object_model_fields(self):
        wikidata_entry_id = "wikidata_entry_id"
        object_model = WikidataLocalizedEntry
        field = 'field'
        value = wikidata_entry_id
        
        try:
            PendingModification.resolve_field_relation(object_model, field, value)
            self.fail()
        except FieldDoesNotExist:
            pass
    
    def test_resolve_field_relation_returns_field_and_destination_value_if_field_is_relation_and_destination_value_exists(self):
        wikidata_entry_id = "wikidata_entry_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        object_model = WikidataLocalizedEntry
        field = 'wikidata_entry__wikidata_id'
        value = wikidata_entry_id
        
        self.assertEqual(('wikidata_entry', wikidata_entry), PendingModification.resolve_field_relation(object_model, field, value))
    
    def test_resolve_field_relation_returns_field_and_destination_value_if_field_is_one_to_one_relation_and_destination_value_exists(self):
        wikidata_entry_id = "wikidata_entry_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        object_model = WikipediaPage
        field = 'wikidata_localized_entry__wikidata_entry__wikidata_id'
        value = wikidata_entry_id
        
        self.assertEqual(('wikidata_localized_entry', wikidata_localized_entry), PendingModification.resolve_field_relation(object_model, field, value))
    
    def test_resolve_field_relation_raises_field_does_not_exist_if_field_is_relation_and_destination_value_does_not_exist(self):
        wikidata_entry_id = "wikidata_entry_id"
        object_model = WikidataLocalizedEntry
        field = 'wikidata_entry__wikidata_id'
        value = wikidata_entry_id
        
        try:
            PendingModification.resolve_field_relation(object_model, field, value)
            self.fail()
        except WikidataEntry.DoesNotExist:
            pass
    
    def test_apply_modification_raises_validation_error_if_target_object_class_is_not_valid(self):
        target_object_class = "target_object_class"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        pending_modification.save()
        
        try:
            pending_modification.apply_modification()
            self.fail()
        except ValidationError:
            pass
    
    def test_apply_modification_raises_validation_error_if_target_object_id_is_not_valid(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = 'target_object_id'
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        pending_modification.save()
        
        try:
            pending_modification.apply_modification()
            self.fail()
        except ValidationError:
            pass
    
    def test_apply_modification_raises_validation_error_if_modified_fields_is_not_valid(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id", "type":"type"}'
        modified_fields = 'modified_fields'
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        pending_modification.save()
        
        try:
            pending_modification.apply_modification()
            self.fail()
        except ValidationError:
            pass
    
    def test_apply_modification_creates_target_object_if_action_is_create_or_update_and_target_object_does_not_exist(self):
        language_code = "language_code"
        wikidata_entry_id = "wikidata_entry_id"
        language_code = "language_code"
        language = Language(code=language_code)
        language.save()
        wikidata_entry_id = "wikidata_entry_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        target_object_class = "WikidataLocalizedEntry"
        target_object_id = '{"wikidata_entry__wikidata_id":"%s", "language__code":"%s"}' % (wikidata_entry_id, language_code)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        pending_modification.save()
        
        pending_modification.apply_modification()
        
        self.assertIsNotNone(WikidataLocalizedEntry.objects.filter(wikidata_entry__wikidata_id=wikidata_entry_id, language__code=language_code).first())
    
    def test_apply_modification_deletes_target_object_if_action_is_delete_and_target_object_exists(self):
        openstreetmap_id = "openstreetmap_id"
        type = "type"
        OpenStreetMapElement(openstreetmap_id=openstreetmap_id, type="type", latitude=0, longitude=0).save()
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s", "type":"%s"}' % (openstreetmap_id, type)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.DELETE)
        pending_modification.save()
        
        pending_modification.apply_modification()
        
        self.assertIsNone(OpenStreetMapElement.objects.filter(openstreetmap_id=openstreetmap_id).first())
    
    def test_apply_modification_sets_modified_fields_values_if_action_is_create_or_update_and_target_object_does_not_exist(self):
        openstreetmap_id = "openstreetmap_id"
        type = "type"
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s", "type":"%s"}' % (openstreetmap_id, type)
        name = "foo"
        sorting_name = "bar"
        modified_fields = '{"name":"%s", "sorting_name":"%s"}' % (name, sorting_name)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        pending_modification.save()
        
        pending_modification.apply_modification()
        openstreetmap_element = OpenStreetMapElement.objects.get(openstreetmap_id=openstreetmap_id)
        
        self.assertEqual(name, openstreetmap_element.name)
        self.assertEqual(sorting_name, openstreetmap_element.sorting_name)
    
    def test_apply_modification_sets_modified_fields_values_if_action_is_create_or_update_and_target_object_exists(self):
        openstreetmap_id = "openstreetmap_id"
        type = "type"
        OpenStreetMapElement(openstreetmap_id=openstreetmap_id, name="name", sorting_name="sorting_name", type="type", latitude=0, longitude=0).save()
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s", "type":"%s"}' % (openstreetmap_id, type)
        name = "foo"
        sorting_name = "bar"
        modified_fields = '{"name":"%s", "sorting_name":"%s"}' % (name, sorting_name)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        pending_modification.save()
        
        pending_modification.apply_modification()
        openstreetmap_element = OpenStreetMapElement.objects.get(openstreetmap_id=openstreetmap_id)
        
        self.assertEqual(name, openstreetmap_element.name)
        self.assertEqual(sorting_name, openstreetmap_element.sorting_name)
    
    def test_apply_modification_converts_none_char_fields_to_empty_char_fields(self):
        openstreetmap_id = "openstreetmap_id"
        type = "type"
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s", "type":"%s"}' % (openstreetmap_id, type)
        modified_fields = '{"name":null}'
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        pending_modification.save()
        
        pending_modification.apply_modification()
        openstreetmap_element = OpenStreetMapElement.objects.get(openstreetmap_id=openstreetmap_id)
        
        self.assertEqual("", openstreetmap_element.name)
    
    def test_apply_modification_deletes_pending_modification_if_modification_is_successful(self):
        openstreetmap_id = "openstreetmap_id"
        type = "type"
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s", "type":"%s"}' % (openstreetmap_id, type)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        pending_modification.save()
        
        pending_modification.apply_modification()
        
        self.assertIsNone(PendingModification.objects.filter(pk=pending_modification.pk).first())
