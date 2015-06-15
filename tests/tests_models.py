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

from superlachaise_api.models import *

class AdminCommandTestCase(TestCase):
    
    def test_admincommand_name_is_unique(self):
        name = u"name"
        AdminCommand(name=name).save()
        
        try:
            AdminCommand(name=name).save()
            self.fail()
        except IntegrityError:
            pass

class LocalizedAdminCommandTestCase(TestCase):
    
    def test_localizedadmincommand_admincommand_and_language_are_unique(self):
        admin_command = AdminCommand(name="name")
        language = Language(code="code")
        LocalizedAdminCommand(admin_command=admin_command, language=language).save()
        
        try:
            LocalizedAdminCommand(admin_command=admin_command, language=language).save()
            self.fail()
        except IntegrityError:
            pass

class LanguageTestCase(TestCase):
    
    def test_language_code_is_unique(self):
        code = u"code"
        Language(code=code).save()
        
        try:
            Language(code=code).save()
            self.fail()
        except IntegrityError:
            pass

class SettingTestCase(TestCase):
    
    def test_setting_key_is_unique(self):
        key = u"key"
        Setting(key=key).save()
        
        try:
            Setting(key=key).save()
            self.fail()
        except IntegrityError:
            pass

class LocalizedSettingTestCase(TestCase):
    
    def test_localizedsetting_setting_and_language_are_unique(self):
        setting = Setting(key="key")
        language = Language(code="code")
        LocalizedSetting(setting=setting, language=language).save()
        
        try:
            LocalizedSetting(setting=setting, language=language).save()
            self.fail()
        except IntegrityError:
            pass

class OpenStreetMapElementTestCase(TestCase):
    
    def test_openstreetmapelement_id_is_unique(self):
        id = u"id"
        OpenStreetMapElement(id=id, type="type1", name="name1", latitude=0, longitude=0).save()
        
        try:
            OpenStreetMapElement(id=id, type="type2", name="name2", latitude=1, longitude=2).save()
            self.fail()
        except IntegrityError:
            pass
