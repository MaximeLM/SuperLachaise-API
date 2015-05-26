# -*- coding: utf-8 -*-

import sys, json
from django.core.management import call_command
from decimal import Decimal
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

def xstr(s):
    if s is None:
        return u''
    return unicode(s)

class SuperLachaiseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Language(SuperLachaiseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class OpenStreetMapPOI(SuperLachaiseModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10,decimal_places=7)
    longitude = models.DecimalField(max_digits=10,decimal_places=7)
    wikipedia = models.CharField(max_length=255,blank=True)
    wikidata = models.CharField(max_length=255,blank=True)
    wikimedia_commons = models.CharField(max_length=255,blank=True)
    historic = models.CharField(max_length=255,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'OpenStreetMap POI'
        verbose_name_plural = u'OpenStreetMap POIs'

class ArchivedModification(SuperLachaiseModel):
    CREATE = u'create'
    MODIFY = u'modify'
    DELETE = u'delete'
    
    action_choices = (
            (CREATE, CREATE),
            (MODIFY, MODIFY),
            (DELETE, DELETE),
        )
    
    target_object_class = models.CharField(max_length=255)
    target_object_id = models.BigIntegerField()
    action = models.CharField(max_length=255, choices=action_choices)
    new_values = models.TextField(blank=True)
    
    def target_model(self):
        try:
            return apps.get_model(self._meta.app_label, self.target_object_class)
        except Exception as exception:
            return None
    
    def target_object(self):
        try:
            return self.target_model().objects.get(id=self.target_object_id)
        except Exception as exception: # TODO 404
            return None
    
    def __unicode__(self):
        return self.action + u': ' + unicode(self.target_object())

class PendingModification(SuperLachaiseModel):
    CREATE = u'create'
    MODIFY = u'modify'
    DELETE = u'delete'
    
    action_choices = (
            (CREATE, CREATE),
            (MODIFY, MODIFY),
            (DELETE, DELETE),
        )
    
    target_object_class = models.CharField(max_length=255)
    target_object_id = models.BigIntegerField()
    action = models.CharField(max_length=255, choices=action_choices)
    new_values = models.TextField(blank=True)
    
    def target_model(self):
        try:
            return apps.get_model(self._meta.app_label, self.target_object_class)
        except Exception as exception:
            return None
    
    def target_object(self):
        try:
            return self.target_model().objects.get(id=self.target_object_id)
        except Exception as exception: # TODO 404
            return None
    
    def clean(self):
        if self.action == u'delete' and not self.target_object():
            raise ValidationError('Target object does not exist')
        if self.action == u'delete' and self.new_values:
            raise ValidationError('Delete actions cannot have new values')
    
    def apply_modification(self):
        if self.action in ['create', 'modify']:
            if self.target_object_class == 'OpenStreetMapPOI':
                openStreetMapPOI = OpenStreetMapPOI.objects.filter(id=self.target_object_id).first()
                if not openStreetMapPOI:
                    openStreetMapPOI = OpenStreetMapPOI(id=self.target_object_id)
                for key, value in json.loads(self.new_values).iteritems():
                    if key == 'name':
                        openStreetMapPOI.name = xstr(value)
                    elif key =='latitude':
                        openStreetMapPOI.latitude = Decimal(value)
                    elif key =='longitude':
                        openStreetMapPOI.longitude = Decimal(value)
                    elif key =='historic':
                        openStreetMapPOI.historic = xstr(value)
                    elif key =='wikipedia':
                        openStreetMapPOI.wikipedia = xstr(value)
                    elif key =='wikidata':
                        openStreetMapPOI.wikidata = xstr(value)
                    elif key =='wikimedia_commons':
                        openStreetMapPOI.wikimedia_commons = xstr(value)
                    else:
                        raise ValidationError('Invalid key {key}'.format(key=key))
                try:
                    openStreetMapPOI.full_clean()
                    openStreetMapPOI.save()
                except Exception as exception:
                    raise ValidationError(exception)
                
            else:
                raise ValidationError('Invalid target object class')
        elif self.action == 'delete':
            target_object = self.target_object()
            if target_object:
                target_object.delete()
        else:
            raise ValidationError('Invalid action')
        
        archivedModification = ArchivedModification(target_object_class=self.target_object_class, target_object_id=self.target_object_id, action=self.action, new_values=self.new_values)
        archivedModification.save()
        self.delete()
    
    def __unicode__(self):
        return self.action + u': ' + unicode(self.target_object())
    
    class Meta:
        unique_together = ('target_object_class', 'target_object_id',)

class Setting(SuperLachaiseModel):
    category = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        unique_together = ('category', 'key',)

class SyncOperation(SuperLachaiseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    last_executed = models.DateTimeField(null=True)
    last_result = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def perform_sync(self):
        call_command('sync_' + self.name)
