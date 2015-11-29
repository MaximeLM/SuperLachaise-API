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

import json, os
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from django.utils.translation import ugettext as _

from superlachaise_api import conf
from superlachaise_api.models import *
from superlachaise_api.views import *

def print_unicode(str):
    print str.encode('utf-8')

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Compute file path
        currentVersion = DBVersion.objects.all().aggregate(Max('version_id'))['version_id__max']
        if not currentVersion:
            raise CommandError(_(u'No DB version found'))
        file_path = settings.STATIC_ROOT + "superlachaise_api/data/data_full_" + str(currentVersion) + ".json"
        if os.path.isfile(file_path):
            raise CommandError(_(u'A full file for this version already exists: ') + file_path)
        
        obj_to_encode = {
            'about': {
                'licence': "https://api.superlachaise.fr/perelachaise/api/licence/",
                'api_version': conf.VERSION,
                'db_version': currentVersion,
                'type': 'full',
            },
            'openstreetmap_elements': OpenStreetMapElement.objects.all().order_by('sorting_name'),
            'wikidata_entries': WikidataEntry.objects.all().order_by('wikidata_id'),
            'wikimedia_commons_categories': WikimediaCommonsCategory.objects.all().order_by('wikimedia_commons_id'),
            'superlachaise_categories': SuperLachaiseCategory.objects.all().order_by('code'),
            'superlachaise_pois': SuperLachaisePOI.objects.all().order_by('openstreetmap_element_id'),
        }
        
        content = SuperLachaiseEncoder(None, languages=Language.objects.all(), restrict_fields=True).encode(obj_to_encode)
        
        with open(file_path, 'w') as full_data_file:
            full_data_file.write(content.encode('utf8'))
