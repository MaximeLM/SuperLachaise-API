# -*- coding: utf-8 -*-

import sys
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

class SuperLachaiseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Language(SuperLachaiseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255,blank=True)
    
    def __unicode__(self):
        return self.name

class OpenStreetMapPOI(SuperLachaiseModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10,decimal_places=7)
    longitude = models.DecimalField(max_digits=10,decimal_places=7)
    wikidata = models.CharField(max_length=255,blank=True)
    wikimedia_commons = models.CharField(max_length=255,blank=True)
    historic = models.CharField(max_length=255,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'OpenStreetMap POI'
        verbose_name_plural = u'OpenStreetMap POIs'

class LocalizedOpenStreetMapPOI(SuperLachaiseModel):
    openStreetMapPOI = models.ForeignKey('OpenStreetMapPOI')
    language = models.ForeignKey('Language')
    wikipedia = models.CharField(max_length=255,blank=True)
    
    def __unicode__(self):
        return self.language.name+":"+self.openStreetMapPOI.name
    
    class Meta:
        unique_together = ('openStreetMapPOI', 'language',)
        verbose_name = u'localized OpenStreetMap POI'
        verbose_name_plural = u'localized OpenStreetMap POIs'

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
    new_values = models.CharField(max_length=255,blank=True)
    apply = models.BooleanField(default=False)
    
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
        if self.apply:
            raise ValidationError('Not yet implemented')
    
    def apply_modification(self):
        self.apply = True
        self.full_clean()
    
    def __unicode__(self):
        return self.action + u': ' + str(self.target_object())
    
    class Meta:
        unique_together = ('target_object_class', 'target_object_id',)

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
    new_values = models.CharField(max_length=255,blank=True)
    
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
        return self.action + u': ' + str(self.target_object())
