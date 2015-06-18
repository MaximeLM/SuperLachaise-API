# -*- coding: utf-8 -*-

"""
tests_synchronization.py
superlachaise_api

Created by Maxime Le Moine on 18/06/2015.
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

from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone
from mock import MagicMock

from superlachaise_api.models import *
from superlachaise_api.synchronization import *

class SynchronizationCommandTestCase(TestCase):
    
    def test_handle_raises_command_error_if_command_name_is_not_set(self):
        try:
            SynchronizationCommand().handle()
            self.fail()
        except CommandError:
            pass
    
    def test_handle_raises_command_error_if_admin_command_with_command_does_not_exist(self):
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = "sync_openstreetmap"
        
        try:
            synchronization_command.handle()
            self.fail()
        except CommandError:
            pass
    
    def test_handle_updates_admin_command_last_executed_if_admin_command_exists(self):
        admin_command_name = "sync_test"
        AdminCommand(name=admin_command_name).save()
        before_sync = timezone.now()
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = admin_command_name
        synchronization_command.synchronize = MagicMock(return_value=None)
        
        synchronization_command.handle()
        
        self.assertTrue(AdminCommand.objects.get(name=admin_command_name).last_executed > before_sync)
    
    def test_handle_calls_synchronize(self):
        admin_command_name = "sync_test"
        AdminCommand(name=admin_command_name).save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = admin_command_name
        synchronization_command.synchronize = MagicMock(return_value=None)
        
        synchronization_command.handle()
        
        self.assertTrue(synchronization_command.synchronize.called)
    
    def test_handle_raises_command_error_if_synchronize_is_not_implemented(self):
        admin_command_name = "sync_test"
        AdminCommand(name=admin_command_name).save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = admin_command_name
        
        try:
            synchronization_command.handle()
            self.fail()
        except CommandError:
            pass
    
    def test_handle_raises_command_error_with_synchronize_error_if_synchronize_raises_error(self):
        admin_command_name = "sync_test"
        AdminCommand(name=admin_command_name).save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = admin_command_name
        error = "error"
        synchronization_command.synchronize = MagicMock(side_effect=Exception(error))
        
        try:
            synchronization_command.handle()
            self.fail()
        except CommandError:
            self.assertEqual(unicode(sys.exc_info()[1]), error)
    
    def test_handle_sets_admin_command_errors_with_synchronize_error_if_synchronize_raises_error(self):
        admin_command_name = "sync_test"
        AdminCommand(name=admin_command_name).save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.command_name = admin_command_name
        error = "error"
        synchronization_command.synchronize = MagicMock(side_effect=Exception(error))
        
        try:
            synchronization_command.handle()
            self.fail()
        except CommandError:
            self.assertEqual(AdminCommand.objects.get(name=admin_command_name).errors, error)
