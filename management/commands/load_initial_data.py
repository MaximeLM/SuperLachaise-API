# -*- coding: utf-8 -*-

"""
load_initial_data.py
superlachaise_api

Created by Maxime Le Moine on 26/05/2015.
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

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.utils.translation import ugettext as _

from superlachaise_api.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        translation.activate(settings.LANGUAGE_CODE)
        
        # Admin commands
        
        admin_command, created = AdminCommand.objects.get_or_create(name="sync_openstreetmap")
        admin_command.dependency_order = 1
        admin_command.description = _("Synchronize OpenStreetMap elements by querying Overpass API for the bouding box and the tags defined in the settings")
        admin_command.save()
        
        admin_command, created = AdminCommand.objects.get_or_create(name="sync_wikidata")
        admin_command.dependency_order = 2
        admin_command.description = _("Synchronize Wikidata entries by querying the codes listed in OpenStreetMap elements")
        admin_command.save()
        
        admin_command, created = AdminCommand.objects.get_or_create(name="sync_wikimedia_commons_categories")
        admin_command.dependency_order = 3
        admin_command.description = _("Synchronize Wikimedia Commons categories by querying the categories listed in OpenStreetMap elements and Wikidata entries")
        admin_command.save()
        
        admin_command, created = AdminCommand.objects.get_or_create(name="sync_wikimedia_commons_files")
        admin_command.dependency_order = 4
        admin_command.description = _("Synchronize Wikimedia Commons files by querying the files listed in Wikimedia Commons categories")
        admin_command.save()
        
        admin_command, created = AdminCommand.objects.get_or_create(name="sync_superlachaise_pois")
        admin_command.dependency_order = 5
        admin_command.description = _("Synchronize SuperLachaise POI by linking OpenStreetMap, Wikidata and Wikimedia Commons objects")
        admin_command.save()
        
        # Languages
        
        language_fr, created = Language.objects.get_or_create(code="fr")
        language_fr.description = _("French")
        language_fr.save()
        
        language_en, created = Language.objects.get_or_create(code="en")
        language_en.description = _("English")
        language_en.save()
        
        # Settings
        
        setting, created = Setting.objects.get_or_create(category="OpenStreetMap", key="auto_apply_modifications")
        setting.value = "false"
        setting.description = _("""If set to 'true', new modifications are applied immediately after being created. If set to 'false', a pending modification is created and must be manually accepted.""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="OpenStreetMap", key="bounding_box")
        setting.value = "48.8575,2.3877,48.8649,2.4006"
        setting.description = _("""The geographical area where to sync OpenStreetMap data : <min lat>,<min lon>,<max lat>,<max lon>""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="OpenStreetMap", key="exclude_ids")
        setting.value = """[{"type": "node", "id": 1688357881}]"""
        setting.description = _("""The OpenStreetMap IDs to exclude from syncing""")
        setting.save()

        setting, created = Setting.objects.get_or_create(category="OpenStreetMap", key="synced_tags")
        setting.value = """["historic=tomb", "historic=memorial"]"""
        setting.description = _("""The OpenStreetMap tags to sync (nodes, ways or relations)""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikidata", key="accepted_locations_of_burial")
        setting.value = """["Q311", "Q3006253"]"""
        setting.description = _("""The list of wikidata codes for cemeteries where to look for tomb data (property P119)""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikidata", key="auto_apply_modifications")
        setting.value = "false"
        setting.description = _("""If set to 'true', new modifications are applied immediately after being created. If set to 'false', a pending modification is created and must be manually accepted.""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikimedia Commons", key="auto_apply_modifications")
        setting.value = "false"
        setting.description = _("""If set to 'true', new modifications are applied immediately after being created. If set to 'false', a pending modification is created and must be manually accepted.""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikimedia Commons", key="synced_instance_of")
        setting.value = """["Q173387", "Q16423655", "Q575759", "Q860861", "Q42948"]"""
        setting.description = _("""The values of 'instance_of' fields of Wikidata entries for which Wikimedia Commons categories should be synced (note: Wikimedia Commons grave categories will always be synced).""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikimedia Commons", key="sync_only_main_image")
        setting.value = "true"
        setting.description = _("""If set to 'true', only the main image from Wikimedia Commons categories will be synced. If set to 'false', all images will be synced.""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="Wikimedia Commons", key="thumbnail_width")
        setting.value = "350"
        setting.description = _("""The thumbnail width to request when syncing Wikimedia Commons files.""")
        setting.save()
        
        setting, created = Setting.objects.get_or_create(category="SuperLachaise POI", key="auto_apply_modifications")
        setting.value = "false"
        setting.description = _("""If set to 'true', new modifications are applied immediately after being created. If set to 'false', a pending modification is created and must be manually accepted.""")
        setting.save()
        
        # Categories
        
        category, created = SuperLachaiseCategory.objects.get_or_create(name=u'tomb')
        category.key = SuperLachaiseCategory.ELEMENT_NATURE
        category.values = ';'.join([u'tomb'])
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_fr, superlachaise_category=category, name=u'Tombes')
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_en, superlachaise_category=category, name=u'Tombs')
        category.save()
        
        category, created = SuperLachaiseCategory.objects.get_or_create(name=u'memorial')
        category.key = SuperLachaiseCategory.ELEMENT_NATURE
        category.values = ';'.join([u'memorial'])
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_fr, superlachaise_category=category, name=u'Mémoriaux')
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_en, superlachaise_category=category, name=u'Memorials')
        category.save()
        
        category, created = SuperLachaiseCategory.objects.get_or_create(name=u'male')
        category.key = SuperLachaiseCategory.SEX_OR_GENDER
        category.values = ';'.join([u'Q6581097'])
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_fr, superlachaise_category=category, name=u'Hommes')
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_en, superlachaise_category=category, name=u'Men')
        category.save()
        
        category, created = SuperLachaiseCategory.objects.get_or_create(name=u'female')
        category.key = SuperLachaiseCategory.SEX_OR_GENDER
        category.values = ';'.join([u'Q6581072'])
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_fr, superlachaise_category=category, name=u'Femmes')
        category.save()
        
        localized_category, created = SuperLachaiseLocalizedCategory.objects.get_or_create(language=language_en, superlachaise_category=category, name=u'Women')
        category.save()
                
        translation.deactivate()
