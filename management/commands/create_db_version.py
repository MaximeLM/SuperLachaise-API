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
from django.db.models import Max
from django.utils import formats, timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

def print_unicode(str):
    print str.encode('utf-8')

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        translation.activate(settings.LANGUAGE_CODE)
        try:
            current_version = DBVersion.objects.all().aggregate(Max('version_id'))['version_id__max']
            current_full_file = settings.STATIC_ROOT + "superlachaise_api/data/data_full_" + str(current_version) + ".json"
            if current_version:
                if not os.path.isfile(current_full_file):
                    raise CommandError(_(u'The full file for the current version does not exist: ') + current_full_file)
            else:
                current_version = 0
            
            # Create new DB version
            print_unicode(_(u'Creating new version...'))
            DBVersion.objects.create(version_id=current_version+1)
            
            # Write full data
            print_unicode(_(u'Writing full file...'))
            call_command("write_full_data")
            
            # Update symbolic link
            full_file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_full_" + str(current_version+1) + ".json"
            latest_file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_full_latest.json"
            command = "ln -s " + full_file_path + " " + latest_file_path
            if os.path.islink(latest_file_path):
                os.remove(latest_file_path)
            os.system(command)
            
            if current_version > 0:
                # Write diff data
                print_unicode(_(u'Writing diff file...'))
                call_command("write_diff_data")
                
                # Delete previous full data
                os.remove(current_full_file)
            
        except:
            print_unicode(traceback.format_exc())
            translation.deactivate()
            raise CommandError(sys.exc_info()[1])
        translation.deactivate()
