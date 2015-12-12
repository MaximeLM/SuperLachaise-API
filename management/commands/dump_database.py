# -*- coding: utf-8 -*-

"""
write_full_data.py
superlachaise_api

Created by Maxime Le Moine on 29/11/2015.
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

import json, errno, os, sys
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.utils import formats, timezone, translation
from django.utils.translation import ugettext as _

from superlachaise_api import conf
from superlachaise_api.models import *
from superlachaise_api.views import *

def print_unicode(str):
    print str.encode('utf-8')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        try:
            obj_to_encode = {
                'about': {
                    'licence': "https://api.superlachaise.fr/perelachaise/api/licence/",
                    'api_version': conf.VERSION,
                },
                'openstreetmap_elements': OpenStreetMapElement.objects.all().order_by('sorting_name'),
                'wikidata_entries': WikidataEntry.objects.all().order_by('wikidata_id'),
                'wikimedia_commons_categories': WikimediaCommonsCategory.objects.all().order_by('wikimedia_commons_id'),
                'superlachaise_categories': SuperLachaiseCategory.objects.all().order_by('code'),
                'superlachaise_pois': SuperLachaisePOI.objects.all().order_by('openstreetmap_element_id'),
            }
        
            content = SuperLachaiseEncoder(None, languages=Language.objects.all(), restrict_fields=True).encode(obj_to_encode)
            
            mkdir_p(settings.DATABASE_DUMP_DIR)
            with open(settings.DATABASE_DUMP_DIR + settings.DATABASE_DUMP_NAME, 'w') as database_dump_file:
                database_dump_file.write(content.encode('utf8'))
            
            if settings.COMMIT_DATABASE_DUMP_DIR:
                if os.path.isdir(settings.DATABASE_DUMP_DIR + ".git"):
                    os.system('cd {0} ; git add . ; git commit -a -m "{1}"'.format(settings.DATABASE_DUMP_DIR, settings.COMMIT_DATABASE_DUMP_MESSAGE))
                    if settings.COMMIT_DATABASE_DUMP_PUSH:
                        os.system('cd {0} ; git push {1}'.format(settings.DATABASE_DUMP_DIR, settings.COMMIT_DATABASE_DUMP_REMOTE_NAME))
                else:
                    print u'Unable to commit database dump dir: ' + settings.DATABASE_DUMP_DIR + '.git does not exist'
        except:
            print_unicode(traceback.format_exc())
            translation.deactivate()
            raise CommandError(sys.exc_info()[1])
        translation.deactivate()
