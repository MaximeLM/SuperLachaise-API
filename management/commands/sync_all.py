# -*- coding: utf-8 -*-

"""
sync_all.py
superlachaise_api

Created by Maxime Le Moine on 10/06/2015.
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

import datetime, os, sys, traceback
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.utils import formats, timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def print_unicode(str):
    print str.encode('utf-8')

class Command(BaseCommand):
    
    def sync_all(self):
        for synchronization in Synchronization.objects.exclude(name=self.synchronization.name).order_by('dependency_order'):
            try:
                call_command(Synchronization.PREFIX + synchronization.name)
            except CommandError:
                print_unicode(traceback.format_exc())
    
    def send_mail_to_managers(self):
        mail_content = []
        
        for synchronization in Synchronization.objects.exclude(name=self.synchronization.name).order_by('dependency_order'):
            if not synchronization.last_executed or synchronization.last_executed < self.start_date:
                mail_content.append(_("{name}: not executed").format(name=synchronization.name))
                mail_content.append('')
            elif (synchronization.created_objects or synchronization.modified_objects or synchronization.deleted_objects or synchronization.errors):
                mail_content.append(_("{name}: executed on {date} at {time}").format(name=synchronization.name, date=formats.date_format(synchronization.last_executed.date(), "SHORT_DATE_FORMAT"), time=formats.time_format(synchronization.last_executed.time(), "TIME_FORMAT")))
                if synchronization.errors:
                    mail_content.append(_('Errors: {errors}').format(errors=synchronization.errors))
                else:
                    if synchronization.created_objects:
                        mail_content.append(_('Created objects: {count}').format(count=synchronization.created_objects))
                    if synchronization.modified_objects:
                        mail_content.append(_('Modified objects: {count}').format(count=synchronization.modified_objects))
                    if synchronization.deleted_objects:
                        mail_content.append(_('Deleted objects: {count}').format(count=synchronization.deleted_objects))
                
                mail_content.append('')
        
        if mail_content:
            end_date = timezone.now()
            duration = end_date - self.start_date
            (minutes, seconds) = divmod(duration.days * 86400 + duration.seconds, 60)
            
            mail_content.append(_('Duration: {minutes} minute(s) and {seconds} second(s)').format(minutes=minutes, seconds=seconds))
            mail_content.append('')
            
            try:
                mail_managers(_('Admin commands results'), '\n'.join(mail_content), fail_silently=False)
            except:
                print_unicode(traceback.format_exc())
                self.errors.append(traceback.format_exc())
    
    def handle(self, *args, **options):
        
        try:
            self.synchronization = Synchronization.objects.get(name=os.path.basename(__file__).split('.')[0].split('sync_')[-1])
        except:
            raise CommandError(sys.exc_info()[1])
        
        error = None
        
        try:
            translation.activate(settings.LANGUAGE_CODE)
            
            self.start_date = timezone.now()
            
            self.created_objects = 0
            self.modified_objects = 0
            self.deleted_objects = 0
            self.errors = []
            
            print_unicode(_('== Start %s ==') % self.synchronization.name)
            self.sync_all()
            self.send_mail_to_managers()
            if settings.DUMP_DATABASE:
                print_unicode(_('Dump database'))
                call_command('dump_database')
            print_unicode(_('== End %s ==') % self.synchronization.name)
            
            self.synchronization.created_objects = self.created_objects
            self.synchronization.modified_objects = self.modified_objects
            self.synchronization.deleted_objects = self.deleted_objects
            self.synchronization.errors = ', '.join(self.errors)
            
            translation.deactivate()
        except:
            print_unicode(traceback.format_exc())
            error = sys.exc_info()[1]
            self.synchronization.errors = traceback.format_exc()
        
        self.synchronization.last_executed = timezone.now()
        self.synchronization.save()
        
        if error:
            raise CommandError(error)
