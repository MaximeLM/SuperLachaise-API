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

import json, traceback
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
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
    
    name = models.CharField(primary_key=True, max_length=255, verbose_name=_('name'))
    dependency_order = models.IntegerField(null=True, verbose_name=_('dependency order'))
    last_executed = models.DateTimeField(null=True, verbose_name=_('last executed'))
    last_result = models.TextField(blank=True, null=True, verbose_name=_('last result'))
    
    def __unicode__(self):
        return self.name
    
    def perform_command(self):
        call_command(str(self.name))
    
    class Meta:
        ordering = ['dependency_order', 'name']
        verbose_name = _('admin command')
        verbose_name_plural = _('admin commands')

class AdminCommandError(SuperLachaiseModel):
    """ An error that occured during an admin command """
    
    target_object_class_choices = (
        ('OpenStreetMapElement', _('openstreetmap element')),
        ('WikidataEntry', _('wikidata entry')),
        ('WikidataLocalizedEntry', _('wikidata localized entry')),
    )
    
    admin_command = models.ForeignKey('AdminCommand', verbose_name=_('admin command'))
    type = models.CharField(max_length=255, blank=True, verbose_name=_('type'))
    description =  models.TextField(blank=True, verbose_name=_('description'))
    target_object_class = models.CharField(max_length=255, blank=True, choices=target_object_class_choices, verbose_name=_('target object class'))
    target_object_id = models.CharField(max_length=255, blank=True, verbose_name=_('target object id'))
    
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
            return unicode(self.admin_command) + u' - ' + self.type + ': ' + unicode(self.target_object())
        else:
            return unicode(self.admin_command) + u' - ' + self.type
    
    class Meta:
        ordering = ['admin_command', 'type', 'target_object_class', 'target_object_id']
        verbose_name = _('admin command error')
        verbose_name_plural = _('admin command errors')

class Language(SuperLachaiseModel):
    """ A language used in the sync operations """
    
    code = models.CharField(primary_key=True, max_length=10, unique=True, verbose_name=_('code'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    enumeration_separator = models.CharField(max_length=255, verbose_name=_('enumeration separator'))
    last_enumeration_separator = models.CharField(max_length=255, verbose_name=_('last enumeration separator'))
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        ordering = ['code']
        verbose_name = _('language')
        verbose_name_plural = _('languages')

class Setting(SuperLachaiseModel):
    """ A custom setting """
    
    key = models.CharField(primary_key=True, max_length=255, verbose_name=_('key'))
    value = models.CharField(max_length=255, blank=True, verbose_name=_('value'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        ordering = ['key']
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

class PendingModification(SuperLachaiseModel):
    """ A modification to an object that is not yet applied """
    
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    
    action_choices = (
        (CREATE, CREATE),
        (MODIFY, MODIFY),
        (DELETE, DELETE),
    )
    
    target_object_class_choices = (
        ('OpenStreetMapElement', _('openstreetmap element')),
        ('WikidataEntry', _('wikidata entry')),
        ('WikimediaCommonsCategory', _('wikimedia commons category')),
        ('WikimediaCommonsFile', _('wikimedia commons file')),
        ('SuperLachaisePOI', _('superlachaise POI')),
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
            if self.target_object_class == 'SuperLachaisePOI':
                result = SuperLachaisePOI.objects.get(openstreetmap_element__id=self.target_object_id)
            else:
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
        
        try:
            if self.action in [self.CREATE, self.MODIFY]:
                # Get or create target object
                target_model = self.target_model()
                target_object = self.target_object()
                if not target_object:
                    if self.target_object_class == 'SuperLachaisePOI':
                        openstreetmap_element = OpenStreetMapElement.objects.get(id=self.target_object_id)
                        target_object = SuperLachaisePOI(openstreetmap_element=openstreetmap_element)
                    else:
                        target_object = target_model(id=self.target_object_id)
            
                localized_objects = {}
                wikidata_entries = None
                categories = None
            
                # Set field values
                for original_field, original_value in json.loads(self.modified_fields).iteritems():
                    object_model = target_model
                    object = target_object
                    field = original_field
                
                    if ':' in field and self.target_object_class in ['WikidataEntry', 'SuperLachaisePOI']:
                    
                        if self.target_object_class == 'WikidataEntry':
                            object_model = apps.get_model(self._meta.app_label, 'WikidataLocalizedEntry')
                        elif self.target_object_class == 'SuperLachaisePOI':
                            object_model = apps.get_model(self._meta.app_label, 'SuperLachaiseLocalizedPOI')
                        if not object_model or object_model == target_model:
                            raise BaseException
                        language = Language.objects.get(code=original_field.split(':')[0])
                    
                        object = None
                        if language.code in localized_objects:
                            object = localized_objects[language.code]
                        if not object:
                            object = target_object.localizations.filter(language=language).first()
                    
                        if original_field == (language.code + u':') and original_value is None:
                            # Delete localization
                            if object:
                                object.delete()
                            continue
                    
                        if not object:
                            if self.target_object_class == 'WikidataEntry':
                                object = object_model(wikidata_entry=target_object, language=language)
                            elif self.target_object_class == 'SuperLachaisePOI':
                                object = object_model(superlachaise_poi=target_object, language=language)
                    
                        if not language.code in localized_objects:
                            localized_objects[language.code] = object
                        field = original_field.split(':')[1]
                
                    if field == 'wikidata_entries' and self.target_object_class == 'SuperLachaisePOI':
                        wikidata_entries = original_value
                        continue
                    
                    if field == 'categories' and self.target_object_class == 'SuperLachaisePOI':
                        categories = original_value
                        continue
                
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
            
                if wikidata_entries:
                    for wikidata_entry_relation in wikidata_entries:
                        relation_type = wikidata_entry_relation.split(':')[0]
                        wikidata_id = wikidata_entry_relation.split(':')[-1]
                        wikidata_entry = WikidataEntry.objects.get(id=wikidata_id)
                        wikidata_entry_relation = target_object.superlachaisewikidatarelation_set.filter(wikidata_entry_id=wikidata_id, relation_type=relation_type).first()
                        if not wikidata_entry_relation:
                            # Create relation
                            wikidata_entry_relation = SuperLachaiseWikidataRelation(superlachaise_poi=target_object, wikidata_entry=wikidata_entry, relation_type=relation_type)
                            wikidata_entry_relation.full_clean()
                            wikidata_entry_relation.save()
                        elif not wikidata_entry_relation.relation_type == relation_type:
                            # Modify relation
                            wikidata_entry_relation.relation_type = relation_type
                            wikidata_entry_relation.full_clean()
                            wikidata_entry_relation.save()
                    for wikidata_entry_relation in target_object.superlachaisewikidatarelation_set.all():
                        relation_str = wikidata_entry_relation.relation_type + u':' + str(wikidata_entry_relation.wikidata_entry_id)
                        if not wikidata_entries or not relation_str in wikidata_entries:
                            # Delete relation
                            wikidata_entry_relation.delete()
                
                if categories:
                    for category_name in categories:
                        category = SuperLachaiseCategory.objects.get(code=category_name)
                        if not category in target_object.categories.all():
                            # Create relation
                            target_object.categories.add(category.code)
                        for category in target_object.categories.all():
                            if not category.code in categories:
                                # Delete relation
                                target_object.categories.remove(category.code)
            
            elif self.action == self.DELETE:
                target_object = self.target_object()
                if target_object:
                    target_object.delete()
            else:
                raise BaseException
            
            self.delete()
        except:
            traceback.print_exc()

class OpenStreetMapElement(SuperLachaiseModel):
    
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
    nature = models.CharField(max_length=255, blank=True, verbose_name=_('nature'))
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name=_('longitude'))
    wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('wikipedia'))
    wikidata = models.CharField(max_length=255, blank=True, verbose_name=_('wikidata'))
    wikidata_combined = models.CharField(max_length=255, blank=True, verbose_name=_('wikidata combined'))
    wikimedia_commons = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['sorting_name', 'id']
        verbose_name = _('openstreetmap element')
        verbose_name_plural = _('openstreetmap elements')

class WikidataEntry(SuperLachaiseModel):
    
    YEAR = 'Year'
    MONTH = 'Month'
    DAY = 'Day'
    
    accuracy_choices = (
        (YEAR, _('Year')),
        (MONTH, _('Month')),
        (DAY, _('Day')),
    )
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    instance_of = models.CharField(max_length=255, blank=True, verbose_name=_('instance of'))
    sex_or_gender = models.CharField(max_length=255, blank=True, verbose_name=_('sex or gender'))
    occupations = models.CharField(max_length=255, blank=True, verbose_name=_('occupations'))
    wikimedia_commons_category = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons category'))
    wikimedia_commons_grave_category = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons grave category'))
    grave_of_wikidata = models.CharField(max_length=255, blank=True, verbose_name=_('grave_of:wikidata'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('date of birth'))
    date_of_death = models.DateField(blank=True, null=True, verbose_name=_('date of death'))
    date_of_birth_accuracy = models.CharField(max_length=255, blank=True, choices=accuracy_choices, verbose_name=_('date of birth accuracy'))
    date_of_death_accuracy = models.CharField(max_length=255, blank=True, choices=accuracy_choices, verbose_name=_('date of death accuracy'))
    burial_plot_reference = models.CharField(max_length=255, blank=True, verbose_name=_('burial plot reference'))
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        verbose_name = _('wikidata entry')
        verbose_name_plural = _('wikidata entries')

class WikidataLocalizedEntry(SuperLachaiseModel):
    """ The part of a wikidata entry specific to a language """
    
    wikidata_entry = models.ForeignKey('WikidataEntry', related_name='localizations', verbose_name=_('wikidata entry'))
    language = models.ForeignKey('Language', verbose_name=_('language'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('wikipedia'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    intro = models.TextField(blank=True, verbose_name=_('intro'))
    
    def __unicode__(self):
        return unicode(self.language) + u':' + self.name
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('wikidata localized entry')
        verbose_name_plural = _('wikidata localized entries')
        unique_together = ('wikidata_entry', 'language',)

class WikimediaCommonsCategory(SuperLachaiseModel):
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    files = models.TextField(blank=True, verbose_name=_('files'))
    main_image = models.CharField(max_length=255, blank=True, verbose_name=_('main image'))
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        verbose_name = _('wikimedia commons category')
        verbose_name_plural = _('wikimedia commons categories')

class WikimediaCommonsFile(SuperLachaiseModel):
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    original_url = models.CharField(max_length=500, blank=True, verbose_name=_('original url'))
    thumbnail_url = models.CharField(max_length=500, blank=True, verbose_name=_('thumbnail url'))
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        verbose_name = _('wikimedia commons file')
        verbose_name_plural = _('wikimedia commons files')

class SuperLachaisePOI(SuperLachaiseModel):
    """ An object linking multiple data sources for representing a single Point Of Interest """
    
    openstreetmap_element = models.OneToOneField('OpenStreetMapElement', unique=True, related_name='superlachaise_poi', verbose_name=_('openstreetmap element'))
    wikidata_entries = models.ManyToManyField('WikidataEntry', related_name='superlachaise_pois', through='SuperLachaiseWikidataRelation', verbose_name=_('wikidata entries'))
    wikimedia_commons_category = models.ForeignKey('WikimediaCommonsCategory', null=True, blank=True, related_name='superlachaise_pois', verbose_name=_('wikimedia commons category'))
    main_image = models.ForeignKey('WikimediaCommonsFile', null=True, blank=True, related_name='superlachaise_pois', verbose_name=_('main image'))
    categories = models.ManyToManyField('SuperLachaiseCategory', blank=True, related_name='superlachaise_pois', verbose_name=_('categories'))
    
    def __unicode__(self):
        return unicode(self.openstreetmap_element)
    
    class Meta:
        ordering = ['openstreetmap_element']
        verbose_name = _('superlachaise POI')
        verbose_name_plural = _('superlachaise POIs')

class SuperLachaiseLocalizedPOI(SuperLachaiseModel):
    """ The part of a SuperLachaise POI specific to a language """
    
    language = models.ForeignKey('Language', verbose_name=_('language'))
    superlachaise_poi = models.ForeignKey('SuperLachaisePOI', related_name='localizations', verbose_name=_('superlachaise poi'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('superlachaise localized POI')
        verbose_name_plural = _('superlachaise localized POIs')

class SuperLachaiseWikidataRelation(SuperLachaiseModel):
    """ A relation between a Super Lachaise POI and a Wikidata entry """
    
    NONE = 'none'
    PERSON = 'person'
    ARTIST = 'artist'
    
    superlachaise_poi = models.ForeignKey('SuperLachaisePOI', verbose_name=_('superlachaise poi'))
    wikidata_entry = models.ForeignKey('WikidataEntry', verbose_name=_('wikidata entry'))
    relation_type = models.CharField(max_length=255, verbose_name=_('relation type'))
    
    def __unicode__(self):
        return self.relation_type + u': ' + unicode(self.superlachaise_poi) + u' - ' + unicode(self.wikidata_entry)
    
    class Meta:
        unique_together = ('superlachaise_poi', 'wikidata_entry', 'relation_type',)
        ordering = ['superlachaise_poi', 'relation_type', 'wikidata_entry']
        verbose_name = _('superlachaisepoi-wikidataentry relationship')
        verbose_name_plural = _('superlachaisepoi-wikidataentry relationships')

class SuperLachaiseCategory(SuperLachaiseModel):
    """ A category for Super Lachaise POIs """
    
    ELEMENT_NATURE = u'element_nature'
    SEX_OR_GENDER = u'sex_or_gender'
    OCCUPATION = u'occupation'
    
    code = models.CharField(primary_key=True, max_length=255, unique=True, verbose_name=_('code'))
    type = models.CharField(max_length=255, verbose_name=_('type'))
    values = models.CharField(max_length=255, blank=True, verbose_name=_('codes'))
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        ordering = ['type', 'code']
        verbose_name = _('superlachaise category')
        verbose_name_plural = _('superlachaise categories')

class SuperLachaiseLocalizedCategory(SuperLachaiseModel):
    """ The part of a SuperLachaise category specific to a language """
    
    language = models.ForeignKey('Language', verbose_name=_('language'))
    superlachaise_category = models.ForeignKey('SuperLachaiseCategory', related_name='localizations', verbose_name=_('superlachaise category'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    
    def __unicode__(self):
        return unicode(self.language) + u':' + self.name
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('superlachaise localized category')
        verbose_name_plural = _('superlachaise localized categories')

class SuperLachaiseOccupation(SuperLachaiseModel):
    """ Associate a person's occupation to a category """
    
    id = models.CharField(primary_key=True, max_length=255, verbose_name=_('id'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    superlachaise_category = models.ForeignKey('SuperLachaiseCategory', null=True, blank=True, limit_choices_to={'type': SuperLachaiseCategory.OCCUPATION}, related_name='occupations', verbose_name=_('superlachaise category'))
    used_in = models.ManyToManyField('WikidataEntry', blank=True, related_name='superlachaise_occupations', verbose_name=_('used in'))
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['id']
        verbose_name = _('superlachaise occupation')
        verbose_name_plural = _('superlachaise occupations')
