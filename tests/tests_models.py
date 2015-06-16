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
    
    def test_openstreetmap_url_returns_none_if_type_is_none(self):
        openstreetmap_id = "123456"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        
        self.assertIsNone(openstreetmap_element.openstreetmap_url())
    
    def test_openstreetmap_url_returns_url_if_type_is_not_none(self):
        openstreetmap_id = "123456"
        type = "node"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id, type=type)
        
        self.assertIsNotNone(openstreetmap_element.openstreetmap_url())
    """
    def test_wikipedia_urls_returns_single_url_if_wikipedia_has_no_semicolon(self):
        openstreetmap_id = "123456"
        wikipedia = "fr:"
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id=openstreetmap_id)
        
        self.assertIsNone(openstreetmap_element.openstreetmap_url())"""

class WikidataEntryTestCase(TestCase):
    
    def test_wikidata_id_is_unique(self):
        wikidata_id = "wikidata_id"
        WikidataEntry(wikidata_id=wikidata_id).save()
        
        try:
            WikidataEntry(wikidata_id=wikidata_id).save()
            self.fail()
        except IntegrityError:
            pass

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

class WikimediaCommonsFileTestCase(TestCase):
    
    def test_wikimedia_commons_id_is_unique(self):
        wikimedia_commons_id = "wikimedia_commons_id"
        WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id).save()
        
        try:
            WikimediaCommonsFile(wikimedia_commons_id=wikimedia_commons_id).save()
            self.fail()
        except IntegrityError:
            pass

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
    
    def test_validation_fails_if_modified_fields_is_not_json(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
        modified_fields = 'modified_fields'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_is_not_json_dict(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
        modified_fields = '["modified_fields"]'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_has_field_not_in_target_object_model_fields(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
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
    
    def test_validation_fails_if_modified_fields_has_id_field(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
        modified_fields = '{"id:5"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        
        try:
            pending_modification.full_clean()
            self.fail()
        except ValidationError:
            pass
    
    def test_validation_fails_if_modified_fields_has_pk_field(self):
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
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
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
        
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
        
        self.assertEqual(None, pending_modification.target_object())
    
    def test_target_object_raises_lookup_error_if_model_does_not_exist(self):
        target_object_class = "target_object_class"
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
        
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id)
        
        try:
            pending_modification.target_object()
            self.fail()
        except LookupError:
            pass
    
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
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
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
        target_object_id = '{"openstreetmap_id":"openstreetmap_id"}'
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
        OpenStreetMapElement(openstreetmap_id=openstreetmap_id).save()
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s"}' % (openstreetmap_id)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.DELETE)
        pending_modification.save()
        
        pending_modification.apply_modification()
        
        self.assertIsNone(OpenStreetMapElement.objects.filter(openstreetmap_id=openstreetmap_id).first())
    
    def test_apply_modification_sets_modified_fields_values_if_action_is_create_or_update_and_target_object_does_not_exist(self):
        openstreetmap_id = "openstreetmap_id"
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s"}' % (openstreetmap_id)
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
        OpenStreetMapElement(openstreetmap_id=openstreetmap_id, name="name", sorting_name="sorting_name").save()
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s"}' % (openstreetmap_id)
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
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s"}' % (openstreetmap_id)
        modified_fields = '{"name":null}'
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE, modified_fields=modified_fields)
        pending_modification.save()
        
        pending_modification.apply_modification()
        openstreetmap_element = OpenStreetMapElement.objects.get(openstreetmap_id=openstreetmap_id)
        
        self.assertEqual("", openstreetmap_element.name)
    
    def test_apply_modification_deletes_pending_modification(self):
        openstreetmap_id = "openstreetmap_id"
        target_object_class = "OpenStreetMapElement"
        target_object_id = '{"openstreetmap_id":"%s"}' % (openstreetmap_id)
        pending_modification = PendingModification(target_object_class=target_object_class, target_object_id=target_object_id, action=PendingModification.CREATE_OR_UPDATE)
        pending_modification.save()
        
        pending_modification.apply_modification()
        
        self.assertIsNone(PendingModification.objects.filter(pk=pending_modification.pk).first())
