# -*- coding: utf-8 -*-

"""
sync_all_and_send_mail_to_managers.py
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

class MailSendingStatus:
    MAIL_SENT, MAIL_NOT_SENT, FAILURE = range(3)

class Command(BaseCommand):
    
    def sync_all(self):
        for admin_command in AdminCommand.objects.exclude(name=self.admin_command.name).order_by('dependency_order'):
            call_command(admin_command.name)
    
    def send_mail_to_managers(self):
        mail_content = []
        
        for admin_command in AdminCommand.objects.exclude(name=self.admin_command.name).order_by('dependency_order'):
            if not admin_command.last_executed or admin_command.last_executed < self.start_date:
                mail_content.append(_("{name}: not executed").format(name=admin_command.name))
                mail_content.append('')
            elif not admin_command.last_result == AdminCommand.NO_MODIFICATIONS:
                mail_content.append(_("{name}: executed on {date} at {time}").format(name=admin_command.name, date=formats.date_format(admin_command.last_executed.date(), "SHORT_DATE_FORMAT"), time=formats.time_format(admin_command.last_executed.time(), "TIME_FORMAT")))
                mail_content.append(_('Result: {result}').format(result=admin_command.last_result))
                mail_content.append('')
        
        if mail_content:
            try:
                mail_managers(_('Admin commands results'), '\n'.join(mail_content), fail_silently=False)
                self.mail_sending_status = MailSendingStatus.MAIL_SENT
            except:
                print_unicode(traceback.format_exc())
                self.mail_sending_status = MailSendingStatus.FAILURE
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        self.admin_command = AdminCommand.objects.get(name=os.path.basename(__file__).split('.')[0])
        error_message = None
        
        try:
            print_unicode(_('== Start %s ==') % self.admin_command.name)
            
            self.start_date = timezone.now()
            self.mail_sending_status = MailSendingStatus.MAIL_NOT_SENT
            self.sync_all()
            self.send_mail_to_managers()
            
            end_date = timezone.now()
            duration = end_date - self.start_date
            (minutes, seconds) = divmod(duration.days * 86400 + duration.seconds, 60)
            
            last_result = []
            
            if self.mail_sending_status == MailSendingStatus.MAIL_NOT_SENT:
                last_result.append(_('Mail not sent'))
            elif self.mail_sending_status == MailSendingStatus.MAIL_SENT:
                last_result.append(_('Mail sent'))
            elif self.mail_sending_status == MailSendingStatus.FAILURE:
                last_result.append(_('Mail sending failure'))
            
            last_result.append(_('Duration: {minutes} minute(s) and {seconds} second(s)').format(minutes=minutes, seconds=seconds))
            
            self.admin_command.last_result = ' ; '.join(last_result)
        except:
            traceback.print_exc()
            exception = sys.exc_info()[0]
            error_message = exception.__class__.__name__ + ': ' + traceback.format_exc()
            self.admin_command.last_result = error_message
        
        print_unicode(_('== End %s ==') % self.admin_command.name)
        
        self.admin_command.last_executed = timezone.now()
        self.admin_command.save()
        
        translation.deactivate()
        
        return error_message
