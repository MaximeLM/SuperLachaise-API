# -*- coding: utf-8 -*-

"""
synchronization.py
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

from __future__ import print_function

import codecs, os, sys, traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class SynchronizationCommand(BaseCommand):
    """ An abstract BaseCommand subclass used to synchronize data """
    
    def log(self, str):
        self.log_file.write(str + '\n')
    
    def synchronize(self):
        """ Override this method to perform the synchronization """
        raise CommandError("synchronize method not implemented by subclass")
    
    def handle(self, *args, **options):
        """ Override this method and set self.command_name before calling super """
        
        try:
            self.log_file = codecs.open(os.path.dirname(__file__) + '/management/logs/log_' + self.command_name, "w", "utf-8")
            self.synchronization = Synchronization.objects.get(name=self.command_name)
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            self.log(_('== Start %s ==') % self.synchronization.name)
            self.synchronize()
            self.log(_('== End %s ==') % self.synchronization.name)
            
            translation.deactivate()
        except:
            self.log(traceback.format_exc())
            error = sys.exc_info()[1]
            self.synchronization.errors = error
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        if error:
            raise CommandError(error)
