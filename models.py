# -*- coding: utf-8 -*-

"""
models.py
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

import json
from decimal import Decimal
from django.apps import apps
from django.core.management import call_command
from django.db import models
from django.utils.translation import ugettext as _

from superlachaise_api.utils import *

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class SuperLachaiseModel(models.Model):
    """ An abstract model with common fields """
    
    notes = models.TextField(blank=True, verbose_name=_('notes'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    
    class Meta:
        abstract = True

class AdminCommand(SuperLachaiseModel):
    """ An admin command that can be monitored """
    
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    last_executed = models.DateTimeField(null=True, verbose_name=_('last executed'))
    last_result = models.TextField(blank=True, null=True, verbose_name=_('last result'))
    
    def __unicode__(self):
        return self.name
    
    def perform_command(self):
        call_command(str(self.name))
    
    class Meta:
        ordering = ['name']
        verbose_name = _('admin command')
        verbose_name_plural = _('admin commands')

class Language(SuperLachaiseModel):
    """ A language used in the sync operations """
    
    code = models.CharField(max_length=10, unique=True, verbose_name=_('code'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        ordering = ['code']
        verbose_name = _('language')
        verbose_name_plural = _('languages')

class OpenStreetMapElement(SuperLachaiseModel):
    """ An OpenStreetMap element """
    
    NODE = 'node'
    WAY = 'way'
    RELATION = 'relation'
    
    type_choices = (
        (NODE, NODE),
        (WAY, WAY),
        (RELATION, RELATION),
    )
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    type = models.CharField(max_length=255, choices=type_choices, verbose_name=_('type'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    sorting_name = models.CharField(max_length=255, blank=True, verbose_name=_('sorting name'))
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name=_('longitude'))
    wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('wikipedia'))
    wikidata = models.CharField(max_length=255, blank=True, verbose_name=_('wikidata'))
    subject_wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('subject:wikipedia'))
    wikimedia_commons = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['sorting_name', 'name']
        verbose_name = _('openstreetmap element')
        verbose_name_plural = _('openstreetmap elements')

class PendingModification(SuperLachaiseModel):
    """ A modification to an object that is not yet applied """
    
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    ERROR = 'error'
    
    action_choices = (
        (CREATE, CREATE),
        (MODIFY, MODIFY),
        (DELETE, DELETE),
        (ERROR, ERROR),
    )
    
    target_object_class_choices = (
        ('OpenStreetMapElement', _('openstreetmap element')),
        ('WikidataEntry', _('wikidata entry')),
        ('WikidataLocalizedEntry', _('wikidata localized entry')),
    )
    
    target_object_class = models.CharField(max_length=255, choices=target_object_class_choices, verbose_name=_('target object class'))
    target_object_id = models.CharField(max_length=255, verbose_name=_('target object id'))
    action = models.CharField(max_length=255, choices=action_choices, verbose_name=_('action'))
    modified_fields = models.TextField(blank=True, verbose_name=_('modified fields'))
    
    def target_model(self):
        """ Returns the model class of the target object """
        try:
            result = apps.get_model(self._meta.app_label, self.target_object_class)
        except:
            result = None
        return result
    
    def target_object(self):
        """ Returns the target object """
        try:
            result = self.target_model().objects.get(id=self.target_object_id)
        except:
            result = None
        return result
    
    def __unicode__(self):
        target_object = self.target_object()
        if target_object:
            return self.action + u': ' + unicode(self.target_object())
        else:
            return self.action
    
    class Meta:
        ordering = ['action', 'target_object_class', 'target_object_id']
        verbose_name = _('pending modification')
        verbose_name_plural = _('pending modifications')
        unique_together = ('target_object_class', 'target_object_id',)
    
    def apply_modification(self):
        """ Apply the modification and delete self """
        
        if self.action in [self.CREATE, self.MODIFY]:
            # Get or create target object
            target_model = self.target_model()
            target_object = target_model.objects.filter(id=self.target_object_id).first()
            if not target_object:
                target_object = target_model(id=self.target_object_id)
            
            localized_objects = {}
            
            # Set field values
            for original_field, original_value in json.loads(self.modified_fields).iteritems():
                object_model = target_model
                object = target_object
                field = original_field
                if ':' in field:
                    object_model = apps.get_model(self._meta.app_label, 'Localized' + self.target_object_class)
                    if not object_model or object_model == target_model:
                        raise BaseException
                    language = Language.objects.get(code=original_field.split(':')[0])
                    
                    object = None
                    if language.code in localized_objects:
                        object = localized_objects[language.code]
                    if not object:
                        object = object_model.objects.filter(parent=target_object, language=language).first()
                    
                    if original_field == (language.code + u':') and original_value is None:
                        # Delete localization
                        if object:
                            object.delete()
                        continue
                    
                    if not object:
                        object = object_model(parent=target_object, language=language)
                    
                    if not language.code in localized_objects:
                        localized_objects[language.code] = object
                    field = original_field.split(':')[1]
                
                if not field in object_model._meta.get_all_field_names():
                    raise BaseException
                field_type = object_model._meta.get_field(field).get_internal_type()
                if field_type == 'CharField':
                    if original_value is None:
                        value = u''
                    else:
                        value = original_value
                elif field_type == 'DecimalField':
                    value = Decimal(original_value)
                else:
                    value = original_value
                setattr(object, field, value)
            
            # Save
            target_object.full_clean()
            target_object.save()
            
            for language_code, localized_object in localized_objects.iteritems():
                localized_object.full_clean()
                localized_object.save()
        
        elif self.action == self.DELETE:
            target_object = self.target_object()
            if target_object:
                target_object.delete()
        elif self.action == self.ERROR:
            pass
        else:
            raise BaseException
        
        self.delete()

class Setting(SuperLachaiseModel):
    """ A custom setting """
    
    category = models.CharField(max_length=255, verbose_name=_('category'))
    key = models.CharField(max_length=255, verbose_name=_('key'))
    value = models.CharField(max_length=255, blank=True, verbose_name=_('value'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return self.category + u':' + self.key
    
    class Meta:
        ordering = ['category', 'key']
        verbose_name = _('setting')
        verbose_name_plural = _('settings')
        unique_together = ('category', 'key',)

class WikidataEntry(SuperLachaiseModel):
    """ A wikidata entry """
    
    YEAR = 'Year'
    MONTH = 'Month'
    DAY = 'Day'
    
    accuracy_choices = (
        (YEAR, YEAR),
        (MONTH, MONTH),
        (DAY, DAY),
    )
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    instance_of = models.CharField(max_length=255, blank=True, verbose_name=_('instance of'))
    wikimedia_commons_category = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons category'))
    wikimedia_commons_grave_category = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons grave category'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('date of birth'))
    date_of_death = models.DateField(blank=True, null=True, verbose_name=_('date of death'))
    date_of_birth_accuracy = models.CharField(max_length=255, blank=True, choices=accuracy_choices, verbose_name=_('date of birth accuracy'))
    date_of_death_accuracy = models.CharField(max_length=255, blank=True, choices=accuracy_choices, verbose_name=_('date of death accuracy'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'id']
        verbose_name = _('wikidata entry')
        verbose_name_plural = _('wikidata entries')

class LocalizedWikidataEntry(SuperLachaiseModel):
    """ The part of a wikidata entry specific to a language """
    
    parent = models.ForeignKey('WikidataEntry')
    language = models.ForeignKey('Language')
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('wikipedia'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return unicode(self.language) + u':' + self.name
    
    class Meta:
        ordering = ['parent', 'language']
        verbose_name = _('localized wikidata entry')
        verbose_name_plural = _('localized wikidata entries')
        unique_together = ('parent', 'language',)
