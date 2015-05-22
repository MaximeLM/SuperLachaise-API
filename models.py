# -*- coding: utf-8 -*-

from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class OpenStreetMapPOI(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10,decimal_places=7)
    longitude = models.DecimalField(max_digits=10,decimal_places=7)
    wikidata = models.CharField(max_length=255,blank=True)
    wikimedia_commons = models.CharField(max_length=255,blank=True)
    historic = models.CharField(max_length=255,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class OpenStreetMapPOILocalization(models.Model):
    openStreetMapPOI = models.ForeignKey('OpenStreetMapPOI')
    language = models.ForeignKey('Language')
    wikipedia = models.CharField(max_length=255,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.language.name+":"+self.openStreetMapPOI.name
    
    class Meta:
        unique_together = ('openStreetMapPOI', 'language',)

class OpenStreetMapPOIModification(models.Model):
    field_choices = (
                    (u'name', u'name'),
                    (u'latitude', u'latitude'),
                    (u'longitude', u'longitude'),
                    (u'wikidata', u'wikidata'),
                    (u'wikimedia_commons', u'wikimedia_commons'),
                    (u'historic', u'historic'),
                    )
    
    openStreetMapPOI = models.ForeignKey('OpenStreetMapPOI')
    field = models.CharField(max_length=255, choices=field_choices)
    new_value_char = models.CharField(max_length=255, blank=True)
    new_value_decimal = models.DecimalField(max_digits=10,decimal_places=7, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.field+":"+self.openStreetMapPOI.name
    
    class Meta:
        unique_together = ('openStreetMapPOI', 'field',)

class OpenStreetMapPOILocalizationModification(models.Model):
    field_choices = (
                    (u'wikipedia', u'wikipedia'),
                    )
    
    openStreetMapPOI = models.ForeignKey('OpenStreetMapPOI')
    language = models.ForeignKey('Language')
    field = models.CharField(max_length=255, choices=field_choices)
    new_value_char = models.CharField(max_length=255, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.field+":"+self.language.name+":"+self.openStreetMapPOI.name
    
    class Meta:
        unique_together = ('openStreetMapPOI', 'language', 'field',)
