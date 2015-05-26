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

from decimal import Decimal
from django.apps import apps
from django.core.management import call_command
from django.db import models
import json

from superlachaise_api.utils import *

class SuperLachaiseModel(models.Model):
    """ An abstract model with common fields """
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class AdminCommand(SuperLachaiseModel):
    """ An admin command that can be monitored """
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    last_executed = models.DateTimeField(null=True)
    last_result = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def perform_command(self):
        call_command(self.name)

class OpenStreetMapPOI(SuperLachaiseModel):
    """ An OpenStreetMap POI """
    
    NODE = 'node'
    WAY = 'way'
    RELATION = 'relation'
    
    type_choices = (
        (NODE, 'node'),
        (WAY, 'way'),
        (RELATION, 'relation'),
    )
    
    id = models.BigIntegerField(primary_key=True)   # redeclared to increase integer precision
    type = models.CharField(max_length=255, choices=type_choices)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    wikipedia = models.CharField(max_length=255, blank=True)
    wikidata = models.CharField(max_length=255, blank=True)
    wikimedia_commons = models.CharField(max_length=255, blank=True)
    historic = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'OpenStreetMap POI'
        verbose_name_plural = u'OpenStreetMap POIs'

class PendingModification(SuperLachaiseModel):
    """ A modification to an object that is not yet applied """
    
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    
    action_choices = (
        (CREATE, u'create'),
        (MODIFY, u'modify'),
        (DELETE, u'delete'),
    )
    
    target_object_class_choices = (
        ('OpenStreetMapPOI', u'OpenStreetMap POI'),
    )
    
    target_object_class = models.CharField(max_length=255, choices=target_object_class_choices)
    target_object_id = models.BigIntegerField()
    action = models.CharField(max_length=255, choices=action_choices)
    modified_fields = models.TextField(blank=True)
    
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
        return self.action + u': ' + unicode(self.target_object())
    
    class Meta:
        unique_together = ('target_object_class', 'target_object_id',)
    
    def apply_modification(self):
        """ Apply the modification and delete self """
        
        if self.action in [self.CREATE, self.MODIFY]:
            # Get or create target object
            target_model = self.target_model()
            target_object = target_model.objects.filter(id=self.target_object_id).first()
            if not target_object:
                target_object = target_model(id=self.target_object_id)
            
            # Set field values
            for field, string_value in json.loads(self.modified_fields).iteritems():
                if not field in target_model._meta.get_all_field_names():
                    raise
                field_type = target_model._meta.get_field(field).get_internal_type()
                if field_type == 'CharField':
                    if string_value is None:
                        value = u''
                    else:
                        value = string_value
                elif field_type == 'DecimalField':
                    value = Decimal(string_value)
                else:
                    raise
                setattr(target_object, field, value)
            
            # Save
            target_object.full_clean()
            target_object.save()
        
        elif self.action == self.DELETE:
            target_object = self.target_object()
            if target_object:
                target_object.delete()
        else:
            raise
        
        self.delete()

class Setting(SuperLachaiseModel):
    """ A custom setting """
    
    category = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.category + u':' + self.key
    
    class Meta:
        unique_together = ('category', 'key',)
