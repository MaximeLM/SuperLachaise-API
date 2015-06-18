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
from django.contrib.messages import ERROR, SUCCESS
from django.contrib.messages.storage.fallback import FallbackStorage
import django.core.management
from django.http import HttpRequest, HttpResponseRedirect
from django.test import TestCase
from django.utils import timezone, translation
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
    
    def mock_call_command(self, return_value=None, side_effect=None):
        django.core.management.call_command = MagicMock(return_value=return_value, side_effect=side_effect)
    
    def test_change_page_url_returns_none_if_object_is_none(self):
        self.assertIsNone(AdminUtils.change_page_url(None))
    
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
        
        self.assertEqual('/admin/superlachaise_api/openstreetmapelement/%s/' % openstreetmap_element.pk, url)
    
    def test_execute_sync_call_command(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, request, args)
        
        self.assertTrue(django.core.management.call_command.called)
    
    def test_execute_sync_call_command_with_command_name(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, request, args)
        
        args = django.core.management.call_command.call_args[0]
        self.assertEqual(command_name, args[0])
    
    def test_execute_sync_add_args_to_command(self):
        command_name = "admin_command"
        args = {
            "arg1": "value1",
            "arg2": "value2",
        }
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, request, args)
        
        kwargs = django.core.management.call_command.call_args[1]
        for arg, value in args.iteritems():
            self.assertEqual(value, kwargs[arg])
    
    def test_execute_sync_add_no_pending_modifications_success_message_to_request_if_command_raises_no_exception_and_command_creates_no_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        self.mock_call_command()
        
        AdminUtils.execute_sync(command_name, request, args)
        
        self.assertEqual(1, len(request._messages))
        for message in request._messages:
            self.assertEqual(SUCCESS, message.level)
            self.assertEqual(AdminUtils.ADMIN_COMMAND_NO_PENDING_MODIFICATIONS_FORMAT, message.message)
    
    def test_execute_sync_add_new_pending_modifications_success_message_to_request_if_command_raises_no_exception_and_command_creates_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        
        def side_effect(*args, **kwargs):
            PendingModification(target_object_class="OpenStreetMapElement", target_object_id='{"openstreetmap_id":"1"}', action=PendingModification.DELETE).save()
        self.mock_call_command(side_effect=side_effect)
        
        AdminUtils.execute_sync(command_name, request, args)
        
        self.assertEqual(1, len(request._messages))
        for message in request._messages:
            self.assertEqual(SUCCESS, message.level)
            self.assertEqual(AdminUtils.ADMIN_COMMAND_NEW_PENDING_MODIFICATIONS_FORMAT.format(count=1), message.message)
    
    def test_execute_sync_add_error_message_with_exception_message_to_request_if_command_raises_exception(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        self.mock_call_command(side_effect=error)
        
        AdminUtils.execute_sync(command_name, request, args)
        
        self.assertEqual(1, len(request._messages))
        for message in request._messages:
            self.assertEqual(ERROR, message.level)
            self.assertEqual(AdminUtils.ADMIN_COMMAND_ERROR_FORMAT.format(command_name=command_name, error=unicode(error)), message.message)
    
    def test_execute_sync_returns_none_if_command_creates_no_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        result = AdminUtils.execute_sync(command_name, request, args)
        
        self.assertIsNone(result)
    
    def test_execute_sync_returns_redirect_to_pending_modifications_filtered_by_created_objects_if_command_creates_pending_modifications(self):
        command_name = "admin_command"
        args = {}
        request = self.dummy_request()
        
        PendingModification(target_object_class="WikidataEntry", target_object_id='{"wikidata_id":"1"}', action=PendingModification.DELETE).save()
        
        def side_effect(*args, **kwargs):
            PendingModification(target_object_class="OpenStreetMapElement", target_object_id='{"openstreetmap_id":"1"}', action=PendingModification.DELETE).save()
        self.mock_call_command(side_effect=side_effect)
        
        result = AdminUtils.execute_sync(command_name, request, args)
        
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, HttpResponseRedirect))
        self.assertTrue(result.url.startswith('/admin/superlachaise_api/pendingmodification/'))
        
        modified_gte_str = re.search(r'^.*modified__gte\=(.*)$', result.url).group(1)
        modified_gte = parse_datetime(urllib.unquote(modified_gte_str).decode('utf8'))
        pending_modifications = PendingModification.objects.filter(modified__gte=modified_gte)
        
        self.assertEqual(1, len(pending_modifications))
        self.assertEqual('OpenStreetMapElement', pending_modifications[0].target_object_class)
    
    def test_current_localization_returns_localized_object_for_current_language_if_localization_for_current_language_exist(self):
        admin_command = AdminCommand(name="name")
        admin_command.save()
        current_language_code = translation.get_language().split("-", 1)[0]
        current_language = Language(code=current_language_code)
        current_language.save()
        other_language = Language(code="other_code")
        other_language.save()
        current_language_localized_admin_command = LocalizedAdminCommand(admin_command=admin_command, language=current_language)
        current_language_localized_admin_command.save()
        other_language_localized_admin_command = LocalizedAdminCommand(admin_command=admin_command, language=other_language)
        other_language_localized_admin_command.save()
        
        self.assertEqual(current_language_localized_admin_command, AdminUtils.current_localization(admin_command))
    
    def test_current_localization_returns_none_if_localization_for_current_language_does_not_exist(self):
        admin_command = AdminCommand(name="name")
        admin_command.save()
        other_language = Language(code="other_code")
        other_language.save()
        other_language_localized_admin_command = LocalizedAdminCommand(admin_command=admin_command, language=other_language)
        other_language_localized_admin_command.save()
        
        self.assertIsNone(AdminUtils.current_localization(admin_command))
    
    def test_delete_notes_empties_notes_for_objects_in_queryset(self):
        AdminCommand(name="name_1", notes="notes_1").save()
        AdminCommand(name="name_2", notes="notes_2").save()
        
        AdminUtils.delete_notes(AdminCommand.objects.all())
        
        for admin_command in AdminCommand.objects.all():
            self.assertEqual("", admin_command.notes)
    
    def test_html_link_returns_none_if_url_is_none(self):
        self.assertIsNone(AdminUtils.html_link(None))
    
    def test_html_link_returns_html_link_format_with_url_and_name_if_url_is_not_none_and_name_is_not_none(self):
        url = 'http://my_url'
        name = 'my_name'
        
        html_link = AdminUtils.html_link(url, name)
        
        self.assertEqual(html_link, AdminUtils.HTML_LINK_FORMAT.format(url=url, name=name))
    
    def test_html_link_returns_html_link_format_with_url_and_url_if_url_is_not_none_and_name_is_none(self):
        url = 'http://my_url'
        
        html_link = AdminUtils.html_link(url)
        
        self.assertEqual(html_link, AdminUtils.HTML_LINK_FORMAT.format(url=url, name=url))
    
    def test_html_link_escapes_quote_in_url(self):
        url = "http://my'_url"
        
        html_link = AdminUtils.html_link(url)
        
        self.assertEqual(html_link, AdminUtils.HTML_LINK_FORMAT.format(url=url.replace("'", "%27"), name=url))
    
    def test_html_image_link_returns_none_if_url_is_none(self):
        image_url = "http://image_url"
        
        self.assertIsNone(AdminUtils.html_image_link(None, image_url))
    
    def test_html_image_link_returns_html_image_link_format_with_url_image_url_width_height_if_url_is_not_none_and_image_url_is_not_none(self):
        url = 'http://my_url'
        image_url = "http://image_url"
        width = 200
        height = 250
        
        html_image_link = AdminUtils.html_image_link(url, image_url, width, height)
        
        self.assertEqual(html_image_link, AdminUtils.HTML_IMAGE_LINK_FORMAT.format(url=url, image_url=image_url, width=width, height=height))
    
    def test_html_image_link_returns_html_image_link_format_with_url_image_url_width_height_if_url_is_not_none_and_image_url_is_none(self):
        url = 'http://my_url'
        width = 200
        height = 250
        
        html_image_link = AdminUtils.html_image_link(url, None, width, height)
        
        self.assertEqual(html_image_link, AdminUtils.HTML_IMAGE_LINK_FORMAT.format(url=url, image_url=url, width=width, height=height))
    
    def test_html_image_link_escapes_quote_in_url(self):
        url = "http://my'_url"
        image_url = "http://image_url"
        width = 200
        height = 250
        
        html_image_link = AdminUtils.html_image_link(url, image_url, width, height)
        
        self.assertEqual(html_image_link, AdminUtils.HTML_IMAGE_LINK_FORMAT.format(url=url.replace("'", "%27"), image_url=image_url, width=width, height=height))
    
    def test_html_image_link_escapes_quote_in_image_url(self):
        url = "http://my_url"
        image_url = "http://image'_url"
        width = 200
        height = 250
        
        html_image_link = AdminUtils.html_image_link(url, image_url, width, height)
        
        self.assertEqual(html_image_link, AdminUtils.HTML_IMAGE_LINK_FORMAT.format(url=url, image_url=image_url.replace("'", "%27"), width=width, height=height))
