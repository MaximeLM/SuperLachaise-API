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

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from superlachaise_api.models import *

class AdminCommandTestCase(TestCase):
    
    def test_name_is_unique(self):
        name = "name"
        AdminCommand(name=name).save()
        
        try:
            AdminCommand(name=name).save()
            self.fail()
        except IntegrityError:
            pass

class LocalizedAdminCommandTestCase(TestCase):
    
    def test_admin_command_and_language_are_unique(self):
        admin_command = AdminCommand(name="name")
        admin_command.save()
        language = Language(code="code")
        language.save()
        LocalizedAdminCommand(admin_command=admin_command, language=language).save()
        
        try:
            LocalizedAdminCommand(admin_command=admin_command, language=language).save()
            self.fail()
        except IntegrityError:
            pass

class LanguageTestCase(TestCase):
    
    def test_code_is_unique(self):
        code = "code"
        Language(code=code).save()
        
        try:
            Language(code=code).save()
            self.fail()
        except IntegrityError:
            pass

class SettingTestCase(TestCase):
    
    def test_key_is_unique(self):
        key = "key"
        Setting(key=key).save()
        
        try:
            Setting(key=key).save()
            self.fail()
        except IntegrityError:
            pass

class LocalizedSettingTestCase(TestCase):
    
    def test_setting_and_language_are_unique(self):
        setting = Setting(key="key")
        setting.save()
        language = Language(code="code")
        language.save()
        LocalizedSetting(setting=setting, language=language).save()
        
        try:
            LocalizedSetting(setting=setting, language=language).save()
            self.fail()
        except IntegrityError:
            pass

class OpenStreetMapElementTestCase(TestCase):
    
    def test_openstreetmap_id_is_unique(self):
        openstreetmap_id = "openstreetmap_id"
        OpenStreetMapElement(openstreetmap_id=openstreetmap_id).save()
        
        try:
            OpenStreetMapElement(openstreetmap_id=openstreetmap_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        openstreetmap_id = "openstreetmap_id"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        openstreetmap_element.save()
        
        query = OpenStreetMapElement.get_object_query_for_id(openstreetmap_id)
        
        self.assertEqual(openstreetmap_element.pk, OpenStreetMapElement.objects.get(query).pk)

class WikidataEntryTestCase(TestCase):
    
    def test_wikidata_id_is_unique(self):
        wikidata_id = "wikidata_id"
        WikidataEntry(wikidata_id=wikidata_id).save()
        
        try:
            WikidataEntry(wikidata_id=wikidata_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikidata_id = "wikidata_id"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_id)
        wikidata_entry.save()
        
        query = WikidataEntry.get_object_query_for_id(wikidata_id)
        
        self.assertEqual(wikidata_entry.pk, WikidataEntry.objects.get(query).pk)

class WikidataLocalizedEntryTestCase(TestCase):
    
    def test_wikidata_entry_and_language_are_unique(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language).save()
        
        try:
            WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikidata_entry_id = "wikidata_entry_id"
        language_code = "code"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        
        query = WikidataLocalizedEntry.get_object_query_for_id("%s:%s" % (wikidata_entry_id, language_code))
        
        self.assertEqual(wikidata_localized_entry.pk, WikidataLocalizedEntry.objects.get(query).pk)
    
    def test_save_updates_wikidata_entry_modified(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        now = timezone.now()
        
        WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language).save()
        
        self.assertTrue(wikidata_entry.modified > now)

class WikipediaPageTestCase(TestCase):
    
    def test_wikidata_localized_entry_is_unique(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        WikipediaPage(wikidata_localized_entry=wikidata_localized_entry).save()
        
        try:
            WikipediaPage(wikidata_localized_entry=wikidata_localized_entry).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikidata_entry_id = "wikidata_id"
        language_code = "code"
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        language = Language(code=language_code)
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage(wikidata_localized_entry=wikidata_localized_entry)
        wikipedia_page.save()
        
        query = WikipediaPage.get_object_query_for_id("%s:%s" % (wikidata_entry_id, language_code))
        
        self.assertEqual(wikipedia_page.pk, WikipediaPage.objects.get(query).pk)
    
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
    
    def test_save_deletes_carriage_returns_in_intro(self):
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        language = Language(code="code")
        language.save()
        wikidata_localized_entry = WikidataLocalizedEntry(wikidata_entry=wikidata_entry, language=language)
        wikidata_localized_entry.save()
        wikipedia_page = WikipediaPage(wikidata_localized_entry=wikidata_localized_entry, intro="intro\r\nnext\n")
        
        wikipedia_page.save()
        
        self.assertFalse('\r' in wikipedia_page.intro)

class WikimediaCommonsCategoryTestCase(TestCase):
    
    def test_wikimedia_commons_id_is_unique(self):
        wikimedia_commons_id = "wikimedia_commons_id"
        WikimediaCommonsCategory(wikimedia_commons_id=wikimedia_commons_id).save()
        
        try:
            WikimediaCommonsCategory(wikimedia_commons_id=wikimedia_commons_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikimedia_commons_id = "wikimedia_commons_id"
        wikimedia_commons_category = WikimediaCommonsCategory(wikimedia_commons_id=wikimedia_commons_id)
        wikimedia_commons_category.save()
        
        query = WikimediaCommonsCategory.get_object_query_for_id(wikimedia_commons_id)
        
        self.assertEqual(wikimedia_commons_category.pk, WikimediaCommonsCategory.objects.get(query).pk)

class WikimediaCommonsFileTestCase(TestCase):
    
    def test_wikimedia_commons_id_is_unique(self):
        wikimedia_commons_id = "wikimedia_commons_id"
        WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id).save()
        
        try:
            WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikimedia_commons_id = "wikimedia_commons_id"
        wikimedia_commons_file = WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id)
        wikimedia_commons_file.save()
        
        query = WikimediaCommonsFile.get_object_query_for_id(wikimedia_commons_id)
        
        self.assertEqual(wikimedia_commons_file.pk, WikimediaCommonsFile.objects.get(query).pk)

class SuperLachaisePOITestCase(TestCase):
    
    def test_openstreetmap_element_is_unique(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        SuperLachaisePOI(openstreetmap_element=openstreetmap_element).save()
        
        try:
            SuperLachaisePOI(openstreetmap_element=openstreetmap_element).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        openstreetmap_element_id = "openstreetmap_element_id"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_element_id)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        
        query = SuperLachaisePOI.get_object_query_for_id(openstreetmap_element_id)
        
        self.assertEqual(superlachaise_poi.pk, SuperLachaisePOI.objects.get(query).pk)

class SuperLachaiseLocalizedPOITestCase(TestCase):
    
    def test_superlachaise_poi_and_language_are_unique(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        language = Language(code="code")
        language.save()
        SuperLachaiseLocalizedPOI(superlachaise_poi=superlachaise_poi, language=language).save()
        
        try:
            SuperLachaiseLocalizedPOI(superlachaise_poi=superlachaise_poi, language=language).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        openstreetmap_element_id = "openstreetmap_element_id"
        language_code = "code"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_element_id)
        openstreetmap_element.save()
        language = Language(code=language_code)
        language.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlaise_localized_poi = SuperLachaiseLocalizedPOI(superlachaise_poi=superlachaise_poi, language=language)
        superlaise_localized_poi.save()
        
        query = SuperLachaiseLocalizedPOI.get_object_query_for_id("%s:%s" % (openstreetmap_element_id, language_code))
        
        self.assertEqual(superlaise_localized_poi.pk, SuperLachaiseLocalizedPOI.objects.get(query).pk)
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        language = Language(code="code")
        language.save()
        now = timezone.now()
        
        SuperLachaiseLocalizedPOI(superlachaise_poi=superlachaise_poi, language=language).save()
        
        self.assertTrue(superlachaise_poi.modified > now)

class SuperLachaiseWikidataRelationTestCase(TestCase):
    
    def test_superlachaise_poi_wikidata_entry_and_relation_type_are_unique(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        relation_type = "relation_type"
        SuperLachaiseWikidataRelation(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type).save()
        
        try:
            SuperLachaiseWikidataRelation(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        openstreetmap_element_id = "openstreetmap_element_id"
        relation_type = "relation_type"
        wikidata_entry_id = "wikidata_entry_id"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_element_id)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        wikidata_entry = WikidataEntry(wikidata_id=wikidata_entry_id)
        wikidata_entry.save()
        superlaise_wikidata_relation = SuperLachaiseWikidataRelation(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type)
        superlaise_wikidata_relation.save()
        
        query = SuperLachaiseWikidataRelation.get_object_query_for_id("%s:%s:%s" % (openstreetmap_element_id, relation_type, wikidata_entry_id))
        
        self.assertEqual(superlaise_wikidata_relation.pk, SuperLachaiseWikidataRelation.objects.get(query).pk)
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        wikidata_entry = WikidataEntry(wikidata_id="wikidata_id")
        wikidata_entry.save()
        relation_type = "relation_type"
        now = timezone.now()
        
        SuperLachaiseWikidataRelation(superlachaise_poi=superlachaise_poi, wikidata_entry=wikidata_entry, relation_type=relation_type).save()
        
        self.assertTrue(superlachaise_poi.modified > now)

class SuperLachaiseCategoryTestCase(TestCase):
    
    def test_code_is_unique(self):
        code = "code"
        SuperLachaiseCategory(code=code).save()
        
        try:
            SuperLachaiseCategory(code=code).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        code = "code"
        superlachaise_category = SuperLachaiseCategory(code=code)
        superlachaise_category.save()
        
        query = SuperLachaiseCategory.get_object_query_for_id(code)
        
        self.assertEqual(superlachaise_category.code, SuperLachaiseCategory.objects.get(query).code)

class SuperLachaiseLocalizedCategoryTestCase(TestCase):
    
    def test_superlachaise_category_and_language_are_unique(self):
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        language = Language(code="code")
        language.save()
        SuperLachaiseLocalizedCategory(superlachaise_category=superlachaise_category, language=language).save()
        
        try:
            SuperLachaiseLocalizedCategory(superlachaise_category=superlachaise_category, language=language).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        superlachaise_category_code = "superlachaise_category_code"
        language_code = "language_code"
        superlachaise_category = SuperLachaiseCategory(code=superlachaise_category_code)
        superlachaise_category.save()
        language = Language(code=language_code)
        language.save()
        superlaise_localized_category = SuperLachaiseLocalizedCategory(superlachaise_category=superlachaise_category, language=language)
        superlaise_localized_category.save()
        
        query = SuperLachaiseLocalizedCategory.get_object_query_for_id("%s:%s" % (superlachaise_category_code, language_code))
        
        self.assertEqual(superlaise_localized_category.pk, SuperLachaiseLocalizedCategory.objects.get(query).pk)
    
    def test_save_updates_superlachaise_category_modified(self):
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        language = Language(code="code")
        language.save()
        superlachaise_category.save()
        now = timezone.now()
        
        SuperLachaiseLocalizedCategory(superlachaise_category=superlachaise_category, language=language).save()
        
        self.assertTrue(superlachaise_category.modified > now)

class SuperLachaiseCategoryRelationTestCase(TestCase):
    
    def test_superlachaise_poi_and_superlachaise_category_are_unique(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        SuperLachaiseCategoryRelation(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category).save()
        
        try:
            SuperLachaiseCategoryRelation(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        openstreetmap_element_id = "openstreetmap_element_id"
        superlachaise_category_code = "superlachaise_category_code"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_element_id)
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlachaise_category = SuperLachaiseCategory(code=superlachaise_category_code)
        superlachaise_category.save()
        superlaise_category_relation = SuperLachaiseCategoryRelation(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category)
        superlaise_category_relation.save()
        
        query = SuperLachaiseCategoryRelation.get_object_query_for_id("%s:%s" % (openstreetmap_element_id, superlachaise_category_code))
        
        self.assertEqual(superlaise_category_relation.pk, SuperLachaiseCategoryRelation.objects.get(query).pk)
    
    def test_save_updates_superlachaise_poi_modified(self):
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        superlachaise_poi = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
        superlachaise_poi.save()
        superlachaise_category = SuperLachaiseCategory(code="code")
        superlachaise_category.save()
        now = timezone.now()
        
        SuperLachaiseCategoryRelation(superlachaise_poi=superlachaise_poi, superlachaise_category=superlachaise_category).save()
        
        self.assertTrue(superlachaise_poi.modified > now)

class WikidataOccupationTestCase(TestCase):
    
    def test_id_is_unique(self):
        wikidata_id = "wikidata_id"
        WikidataOccupation(wikidata_id=wikidata_id).save()
        
        try:
            WikidataOccupation(wikidata_id=wikidata_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_get_object_query_for_id_returns_valid_query(self):
        wikidata_id = "wikidata_id"
        wikidata_occupation = WikidataOccupation(wikidata_id=wikidata_id)
        wikidata_occupation.save()
        
        query = WikidataOccupation.get_object_query_for_id(wikidata_id)
        
        self.assertEqual(wikidata_occupation.pk, WikidataOccupation.objects.get(query).pk)

class PendingModificationTestCase(TestCase):
    
    def test_target_object_class_and_target_object_id_are_unique(self):
        target_object_class = "target_object_class"
        target_object_id = "target_object_id"
        PendingModification(target_object_class=target_object_class, target_object_id=target_object_id).save()
        
        try:
            PendingModification(target_object_class=target_object_class, target_object_id=target_object_id).save()
            self.fail()
        except IntegrityError:
            pass
    
    def test_target_object_model_returns_valid_class(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = "target_object_id"
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertEqual(OpenStreetMapElement, pending_modification.target_object_model())
    
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
        target_object_id = "%s:%s" % (wikidata_entry_id, language_code)
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        self.assertEqual(wikidata_localized_entry.pk, pending_modification.target_object().pk)
