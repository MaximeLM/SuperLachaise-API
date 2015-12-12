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
        openstreetmap_element = OpenStreetMapElement(openstreetmap_id="openstreetmap_id", type="type", latitude=0, longitude=0)
        openstreetmap_element.save()
        
        url = AdminUtils.change_page_url(openstreetmap_element)
        
        self.assertEqual('/admin/superlachaise_api/openstreetmapelement/%s/change/' % openstreetmap_element.pk, url)
    
    def test_changelist_page_url_returns_admin_url_with_model(self):
        model = OpenStreetMapElement
        
        url = AdminUtils.changelist_page_url(model)
        
        self.assertEqual('/admin/superlachaise_api/openstreetmapelement/', url)
    
    def test_execute_sync_calls_call_command(self):
        synchronization_name = "synchronization"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(synchronization_name, request, args)
        
        self.assertTrue(django.core.management.call_command.called)
    
    def test_execute_sync_call_command_with_prefixed_synchronization_name(self):
        synchronization_name = "synchronization"
        args = {}
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(synchronization_name, request, args)
        
        args = django.core.management.call_command.call_args[0]
        self.assertEqual(Synchronization.PREFIX + synchronization_name, args[0])
    
    def test_execute_sync_add_args_to_command(self):
        synchronization_name = "synchronization"
        args = {
            "arg1": "value1",
            "arg2": "value2",
        }
        request = self.dummy_request()
        self.mock_call_command()
        
        AdminUtils.execute_sync(synchronization_name, request, args)
        
        kwargs = django.core.management.call_command.call_args[1]
        for arg, value in args.iteritems():
            self.assertEqual(value, kwargs[arg])
    
    def test_execute_sync_add_success_message_to_request_if_command_raises_no_exception(self):
        synchronization_name = "synchronization"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        self.mock_call_command()
        
        AdminUtils.execute_sync(synchronization_name, request, args)
        
        self.assertEqual(1, len(request._messages))
        for message in request._messages:
            self.assertEqual(SUCCESS, message.level)
            self.assertEqual(AdminUtils.EXECUTE_SYNC_DONE_FORMAT.format(synchronization_name=synchronization_name), message.message)
    
    def test_execute_sync_add_error_message_with_exception_message_to_request_if_command_raises_exception(self):
        synchronization_name = "synchronization"
        args = {}
        request = self.dummy_request()
        error = Exception("error")
        self.mock_call_command(side_effect=error)
        
        AdminUtils.execute_sync(synchronization_name, request, args)
        
        self.assertEqual(1, len(request._messages))
        for message in request._messages:
            self.assertEqual(ERROR, message.level)
            self.assertEqual(AdminUtils.EXECUTE_SYNC_ERROR_FORMAT.format(synchronization_name=synchronization_name, error=unicode(error)), message.message)
    
    def test_current_localization_returns_localized_object_for_current_language_if_localization_for_current_language_exist(self):
        synchronization = Synchronization(name="name")
        synchronization.save()
        current_language_code = translation.get_language().split("-", 1)[0]
        current_language = Language(code=current_language_code)
        current_language.save()
        other_language = Language(code="other_code")
        other_language.save()
        current_language_localized_synchronization = LocalizedSynchronization(synchronization=synchronization, language=current_language)
        current_language_localized_synchronization.save()
        other_language_localized_synchronization = LocalizedSynchronization(synchronization=synchronization, language=other_language)
        other_language_localized_synchronization.save()
        
        self.assertEqual(current_language_localized_synchronization, AdminUtils.current_localization(synchronization))
    
    def test_current_localization_returns_none_if_localization_for_current_language_does_not_exist(self):
        synchronization = Synchronization(name="name")
        synchronization.save()
        other_language = Language(code="other_code")
        other_language.save()
        other_language_localized_synchronization = LocalizedSynchronization(synchronization=synchronization, language=other_language)
        other_language_localized_synchronization.save()
        
        self.assertIsNone(AdminUtils.current_localization(synchronization))
    
    def test_delete_notes_empties_notes_for_objects_in_queryset(self):
        Synchronization(name="name_1", notes="notes_1").save()
        Synchronization(name="name_2", notes="notes_2").save()
        
        AdminUtils.delete_notes(Synchronization.objects.all())
        
        for synchronization in Synchronization.objects.all():
            self.assertEqual("", synchronization.notes)
    
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
    
    def test_date_with_accuracy_returns_none_if_date_is_none(self):
        date = None
        accuracy = 'Day'
        
        self.assertIsNone(AdminUtils.date_with_accuracy(date, accuracy))
    
    def test_date_with_accuracy_returns_date_without_accuracy_if_date_is_not_none_and_accuracy_is_empty(self):
        date = timezone.now().date()
        accuracy = ''
        
        self.assertEqual(AdminUtils.date_with_accuracy(date, accuracy), AdminUtils.DATE_WITHOUT_ACCURACY_FORMAT.format(date=date))
    
    def test_date_with_accuracy_returns_date_with_accuracy_if_date_is_not_none_and_accuracy_is_not_empty(self):
        date = timezone.now().date()
        accuracy = 'Day'
        
        self.assertEqual(AdminUtils.date_with_accuracy(date, accuracy), AdminUtils.DATE_WITH_ACCURACY_FORMAT.format(date=date, accuracy=accuracy))
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_none_if_name_is_none(self):
        name = None
        sorting_name = 'my_sorting_name'
        
        self.assertIsNone(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name))
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_name_if_sorting_name_is_none(self):
        name = 'my_first_name my_name'
        sorting_name = None
        
        self.assertEqual(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name), name)
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_name_if_sorting_name_is_empty(self):
        name = 'my_first_name my_name'
        sorting_name = ''
        
        self.assertEqual(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name), name)
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_name_if_first_part_of_sorting_name_splitted_by_comma_is_not_in_name(self):
        name = 'my_first_name my_name'
        sorting_name = 'my_name my_first_name'
        
        self.assertEqual(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name), name)
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_name_with_first_letter_of_sorting_name_in_bold_if_first_part_of_sorting_name_splitted_by_comma_is_in_name(self):
        name = 'my_first_name my_name'
        sorting_name = 'my_name, my_first_name'
        
        self.assertEqual(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name), 'my_first_name <b>m</b>y_name')
    
    def test_name_with_bold_first_letter_of_sorting_name_returns_name_with_first_letter_of_last_occurence_of_sorting_name_in_bold_if_first_part_of_sorting_name_splitted_by_comma_is_multiple_times_in_name(self):
        name = 'my_name my_name'
        sorting_name = 'my_name, my_first_name'
        
        self.assertEqual(AdminUtils.name_with_bold_first_letter_of_sorting_name(name, sorting_name), 'my_name <b>m</b>y_name')
