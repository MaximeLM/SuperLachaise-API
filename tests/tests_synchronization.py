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
from mock import MagicMock, patch

from superlachaise_api.models import *
from superlachaise_api.synchronization import *
from superlachaise_api.management.commands.sync_openstreetmap import Command as SyncOpenStreetMapCommand

class SynchronizationCommandTestCase(TestCase):
    
    def test_execute_sets_synchronization(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        before_sync = timezone.now()
        synchronization_command = SynchronizationCommand()
        synchronization_command.synchronize = MagicMock(return_value=None)
        
        synchronization_command.execute(synchronization)
        
        self.assertEqual(synchronization_command.synchronization, synchronization)
    
    def test_execute_updates_synchronization_last_executed(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        before_sync = timezone.now()
        synchronization_command = SynchronizationCommand()
        synchronization_command.synchronize = MagicMock(return_value=None)
        
        synchronization_command.execute(synchronization)
        
        self.assertTrue(Synchronization.objects.get(name=synchronization.name).last_executed > before_sync)
    
    def test_execute_calls_synchronize(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.synchronize = MagicMock(return_value=None)
        
        synchronization_command.execute(synchronization)
        
        self.assertTrue(synchronization_command.synchronize.called)
    
    def test_execute_raises_command_error_if_synchronize_is_not_implemented(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        synchronization_command = SynchronizationCommand()
        synchronization_command.synchronization = synchronization
        
        try:
            synchronization_command.execute(synchronization)
            self.fail()
        except CommandError:
            pass
    
    def test_execute_raises_command_error_with_synchronize_error_if_synchronize_raises_error(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        synchronization_command = SynchronizationCommand()
        error = "error"
        synchronization_command.synchronize = MagicMock(side_effect=Exception(error))
        
        try:
            synchronization_command.execute(synchronization)
            self.fail()
        except CommandError:
            self.assertEqual(unicode(sys.exc_info()[1]), error)
    
    def test_execute_sets_synchronization_errors_with_synchronize_error_if_synchronize_raises_error(self):
        synchronization = Synchronization(name="test")
        synchronization.save()
        synchronization_command = SynchronizationCommand()
        error = "error"
        synchronization_command.synchronize = MagicMock(side_effect=Exception(error))
        
        try:
            synchronization_command.execute(synchronization)
            self.fail()
        except CommandError:
            self.assertEqual(Synchronization.objects.get(name=synchronization.name).errors, error)

class SyncOpenStreetMapTestCase(TestCase):
    
    def setUp(self):
        self.synchronization_name = "openstreetmap"
        self.synchronization = Synchronization.objects.create(name=self.synchronization_name)
    
    @patch.object(SynchronizationCommand, 'execute')
    def test_handle_calls_execute_with_openstreetmap_synchronization(self, mock):
        command = SyncOpenStreetMapCommand()
        command.synchronize = MagicMock(return_value=None)
        
        command.handle()
        
        self.assertTrue(mock.called)
        self.assertTrue(isinstance(mock.call_args[0][0], Synchronization))
        self.assertEqual(mock.call_args[0][0].name, self.synchronization_name)
