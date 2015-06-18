# -*- coding: utf-8 -*-

"""
tests_admin.py
superlachaise_api

Created by Maxime Le Moine on 17/06/2015.
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

import re, urllib
from django.contrib.messages import ERROR
from django.contrib.messages.storage.fallback import FallbackStorage
import django.core.management
from django.http import HttpRequest, HttpResponseRedirect
from django.test import TestCase
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from mock import MagicMock

from superlachaise_api.models import *
from superlachaise_api.admin import *

class AdminUtilsTestCase(TestCase):
    
    def dummy_request(self):
        request = HttpRequest()
        
        # http://stackoverflow.com/questions/11938164/why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request
    
    def mock_call_command(self, side_effect=None):
        django.core.management.call_command = MagicMock(side_effect=side_effect)
    
    def test_change_page_url_returns_none_if_object_is_not_saved(self):
        model = OpenStreetMapElement
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        
        url = AdminUtils.change_page_url(openstreetmap_element)
        
        self.assertIsNone(url)
    
    def test_change_page_url_returns_admin_url_with_object_model_and_pk_if_object_is_saved(self):
        model = OpenStreetMapElement
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id")
        openstreetmap_element.save()
        
        url = AdminUtils.change_page_url(openstreetmap_element)
        
        self.assertEqual(url, '/admin/superlachaise_api/openstreetmapelement/%s/' % openstreetmap_element.pk)
    
    def test_execute_sync_call_command(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, args, request)
        
        self.assertTrue(django.core.management.call_command.called)
    
    def test_execute_sync_call_command_with_command_name(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, args, request)
        
        args = django.core.management.call_command.call_args[0]
        self.assertEqual(args[0], command_name)
    
    def test_execute_sync_add_args_to_command(self):
        command_name = "admin_command"
        args = {
            "arg1": "value1",
            "arg2": "value2",
        }
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, args, request)
        
        kwargs = django.core.management.call_command.call_args[1]
        for arg, value in args.iteritems():
            self.assertEqual(kwargs[arg], value)
    
    def test_execute_sync_add_error_message_with_exception_message_to_request_if_command_raises_exception(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        self.mock_call_command(side_effect=error)
        
        AdminUtils.execute_sync(command_name, args, request)
        
        self.assertEqual(len(request._messages), 1)
        for message in request._messages:
            self.assertEqual(message.level, ERROR)
            self.assertEqual(message.message, AdminUtils.ADMIN_COMMAND_ERROR_TEMPLATE.format(command_name=command_name, error=unicode(error)))
    
    def test_execute_sync_returns_none_if_command_creates_no_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        result = AdminUtils.execute_sync(command_name, args, request)
        
        self.assertIsNone(result)
    
    def test_execute_sync_returns_redirect_to_pending_modifications_filtered_by_created_objects_if_command_creates_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        
        PendingModification(target_object_class="WikidataEntry", target_object_id='{"wikidata_id":"1"}', action=PendingModification.DELETE).save()
        
        def side_effect(*args, **kwargs):
            PendingModification(target_object_class="OpenStreetMapElement", target_object_id='{"openstreetmap_id":"1"}', action=PendingModification.DELETE).save()
        self.mock_call_command(side_effect=side_effect)
        
        result = AdminUtils.execute_sync(command_name, args, request)
        
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, HttpResponseRedirect))
        self.assertTrue(result.url.startswith('/admin/superlachaise_api/pendingmodification/'))
        
        modified_gte_str = re.search(r'^.*modified__gte\=(.*)$', result.url).group(1)
        modified_gte = parse_datetime(urllib.unquote(modified_gte_str).decode('utf8'))
        pending_modifications = PendingModification.objects.filter(modified__gte=modified_gte)
        
        self.assertEqual(len(pending_modifications), 1)
        self.assertEqual(pending_modifications[0].target_object_class, 'OpenStreetMapElement')
