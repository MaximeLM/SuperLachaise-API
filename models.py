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
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import models
from django.utils.translation import ugettext as _

class SuperLachaiseModel(models.Model):
    """ An abstract model with common fields """
    
    notes = models.TextField(blank=True, verbose_name=_('notes'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    
    class Meta:
        abstract = True

class Synchronization(SuperLachaiseModel):
    """ An synchronization admin command that can be monitored """
    
    PREFIX = 'sync_'
    
    name = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('name'))
    dependency_order = models.IntegerField(null=True, blank=True, verbose_name=_('dependency order'))
    last_executed = models.DateTimeField(blank=True, null=True, verbose_name=_('last executed'))
    created_objects = models.IntegerField(default=0, verbose_name=_('created objects'))
    modified_objects = models.IntegerField(default=0, verbose_name=_('modified objects'))
    deleted_objects = models.IntegerField(default=0, verbose_name=_('deleted objects'))
    errors = models.TextField(blank=True, null=True, verbose_name=_('errors'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['dependency_order', 'name']
        verbose_name = _('synchronization')
        verbose_name_plural = _('synchronizations')

class LocalizedSynchronization(SuperLachaiseModel):
    """ The part of a Synchronization specific to a language """
    
    language = models.ForeignKey('Language', verbose_name=_('language'))
    synchronization = models.ForeignKey('Synchronization', related_name='localizations', verbose_name=_('synchronization'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return unicode(self.synchronization) + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'synchronization']
        verbose_name = _('localized synchronization')
        verbose_name_plural = _('localized synchronizations')
        unique_together = ('synchronization', 'language',)

class Language(SuperLachaiseModel):
    """ A language used in the sync operations """
    
    code = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('code'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    enumeration_separator = models.CharField(max_length=255, verbose_name=_('enumeration separator'))
    last_enumeration_separator = models.CharField(max_length=255, verbose_name=_('last enumeration separator'))
    artist_prefix = models.CharField(max_length=255, verbose_name=_('artist prefix'))
    
    def __unicode__(self):
        if self.description:
            return self.description
        else:
            return self.code
    
    class Meta:
        ordering = ['code']
        verbose_name = _('language')
        verbose_name_plural = _('languages')

class Setting(SuperLachaiseModel):
    """ A custom setting """
    
    key = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('key'))
    value = models.CharField(max_length=255, blank=True, verbose_name=_('value'))
    default = models.CharField(max_length=255, blank=True, verbose_name=_('default'))
    
    def __unicode__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        # Set value with default if empty
        if not self.value:
            self.value = self.default
        super(Setting, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['key']
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

class LocalizedSetting(SuperLachaiseModel):
    """ The part of a Setting specific to a language """
    
    language = models.ForeignKey('Language', verbose_name=_('language'))
    setting = models.ForeignKey('Setting', related_name='localizations', verbose_name=_('setting'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return unicode(self.setting) + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'setting']
        verbose_name = _('localized setting')
        verbose_name_plural = _('localized settings')
        unique_together = ('setting', 'language',)

class OpenStreetMapElement(SuperLachaiseModel):
    
    URL_FORMAT = u'https://www.openstreetmap.org/{type}/{id}'
    
    NODE = 'node'
    WAY = 'way'
    RELATION = 'relation'
    
    type_choices = (
        (NODE, NODE),
        (WAY, WAY),
        (RELATION, RELATION),
    )
    
    openstreetmap_id = models.CharField(db_index=True, max_length=255, verbose_name=_('openstreetmap id'))
    type = models.CharField(max_length=255, db_index=True, choices=type_choices, verbose_name=_('type'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    sorting_name = models.CharField(max_length=255, blank=True, verbose_name=_('sorting name'))
    nature = models.CharField(max_length=255, blank=True, verbose_name=_('nature'))
    latitude = models.DecimalField(max_digits=10, default=0, decimal_places=7, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=10, default=0, decimal_places=7, verbose_name=_('longitude'))
    wikidata = models.CharField(max_length=255, blank=True, verbose_name=_('wikidata'))
    wikimedia_commons = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons'))
    
    def openstreetmap_url(self):
        if self.type:
            return OpenStreetMapElement.URL_FORMAT.format(type=self.type, id=self.openstreetmap_id)
    
    def wikidata_list(self):
        if self.wikidata:
            return self.wikidata.split(';')
    
    def wikidata_url(self, language_code, wikidata):
        return WikidataEntry.URL_FORMAT.format(id=wikidata.split(':')[-1], language_code=language_code)
    
    def wikimedia_commons_url(self):
        if self.wikimedia_commons:
            return WikimediaCommonsCategory.URL_FORMAT.format(title=self.wikimedia_commons)
    
    def __unicode__(self):
        return self.name if self.name else u'[%s]' % self.openstreetmap_id
    
    class Meta:
        ordering = ['sorting_name', 'openstreetmap_id']
        verbose_name = _('openstreetmap element')
        verbose_name_plural = _('openstreetmap elements')
        unique_together = ('type', 'openstreetmap_id',)

class WikidataEntry(SuperLachaiseModel):
    
    URL_FORMAT = u'https://www.wikidata.org/wiki/{id}?userlang={language_code}&uselang={language_code}'
    
    YEAR = 'Year'
    MONTH = 'Month'
    DAY = 'Day'
    
    accuracy_choices = (
        (YEAR, _('Year')),
        (MONTH, _('Month')),
        (DAY, _('Day')),
    )
    
    wikidata_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('wikidata id'))
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
    
    def wikidata_list(self, field):
        value = getattr(self, field)
        if value:
            return value.split(';')
    
    def wikidata_url(self, language_code, wikidata):
        return WikidataEntry.URL_FORMAT.format(id=wikidata, language_code=language_code)
    
    def wikimedia_commons_category_url(self, field):
        value = getattr(self, field)
        if value:
            return WikimediaCommonsCategory.URL_FORMAT.format(title=u'Category:%s' % value)
    
    def __unicode__(self):
        return self.wikidata_id
    
    class Meta:
        ordering = ['wikidata_id']
        verbose_name = _('wikidata entry')
        verbose_name_plural = _('wikidata entries')

class WikidataLocalizedEntry(SuperLachaiseModel):
    """ The part of a wikidata entry specific to a language """
    
    wikidata_entry = models.ForeignKey('WikidataEntry', related_name='localizations', verbose_name=_('wikidata entry'))
    language = models.ForeignKey('Language', verbose_name=_('language'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    wikipedia = models.CharField(max_length=255, blank=True, verbose_name=_('wikipedia'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def wikipedia_url(self):
        if self.wikipedia:
            return WikipediaPage.URL_FORMAT.format(language_code=self.language.code, title=self.wikipedia)
    
    def save(self, *args, **kwargs):
        super(WikidataLocalizedEntry, self).save(*args, **kwargs)
        
        # Touch Wikidata entry
        self.wikidata_entry.save()
    
    def delete(self):
        # Touch Wikidata entry
        self.wikidata_entry.save()
        
        super(WikidataLocalizedEntry, self).delete()
    
    def __unicode__(self):
        return self.name + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('wikidata localized entry')
        verbose_name_plural = _('wikidata localized entries')
        unique_together = ('wikidata_entry', 'language',)

class WikipediaPage(SuperLachaiseModel):
    
    URL_FORMAT = u'https://{language_code}.wikipedia.org/wiki/{title}'
    
    wikidata_localized_entry = models.OneToOneField('WikidataLocalizedEntry', related_name='wikipedia_page', verbose_name=_('wikidata localized entry'))
    default_sort = models.CharField(max_length=255, blank=True, verbose_name=_('default sort'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    intro = models.TextField(blank=True, verbose_name=_('intro'))
    
    def clean(self):
        # Delete \r added by textfield
        self.intro = self.intro.replace('\r','')
    
    def save(self, *args, **kwargs):
        super(WikipediaPage, self).save(*args, **kwargs)
        
        # Touch Wikidata localized entry
        self.wikidata_localized_entry.save()
    
    def delete(self):
        # Touch Wikidata localized entry
        self.wikidata_localized_entry.save()
        
        super(WikipediaPage, self).delete()
    
    def __unicode__(self):
        return self.wikidata_localized_entry.wikipedia + u' (' + unicode(self.wikidata_localized_entry.language) + u')'
    
    class Meta:
        ordering = ['default_sort', 'wikidata_localized_entry']
        verbose_name = _('wikipedia page')
        verbose_name_plural = _('wikipedia pages')

class WikimediaCommonsCategory(SuperLachaiseModel):
    
    URL_FORMAT = u'https://commons.wikimedia.org/wiki/{title}'
    
    wikimedia_commons_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('wikimedia commons id'))
    main_image = models.CharField(max_length=255, blank=True, verbose_name=_('main image'))
    category_members = models.TextField(blank=True, verbose_name=_('category members'))
    
    def category_members_list(self):
        if self.category_members:
            return self.category_members.split('|')
        else:
            return []
    
    def wikimedia_commons_url(self, field_value):
        if field_value:
            return WikimediaCommonsCategory.URL_FORMAT.format(title=field_value)
    
    def __unicode__(self):
        return self.wikimedia_commons_id
    
    class Meta:
        ordering = ['wikimedia_commons_id']
        verbose_name = _('wikimedia commons category')
        verbose_name_plural = _('wikimedia commons categories')

class WikimediaCommonsFile(SuperLachaiseModel):
    
    wikimedia_commons_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('wikimedia commons id'))
    original_url = models.CharField(max_length=500, blank=True, verbose_name=_('original url'))
    thumbnail_url = models.CharField(max_length=500, blank=True, verbose_name=_('thumbnail url'))
    
    def wikimedia_commons_url(self):
        return WikimediaCommonsCategory.URL_FORMAT.format(title=self.wikimedia_commons_id)
    
    def __unicode__(self):
        return self.wikimedia_commons_id
    
    class Meta:
        ordering = ['wikimedia_commons_id']
        verbose_name = _('wikimedia commons file')
        verbose_name_plural = _('wikimedia commons files')

class SuperLachaisePOI(SuperLachaiseModel):
    """ An object linking multiple data sources for representing a single Point Of Interest """
    
    openstreetmap_element = models.OneToOneField('OpenStreetMapElement', blank=True, null=True, on_delete=models.SET_NULL, unique=True, related_name='superlachaise_poi', verbose_name=_('openstreetmap element'))
    wikidata_entries = models.ManyToManyField('WikidataEntry', related_name='superlachaise_pois', through='SuperLachaiseWikidataRelation', verbose_name=_('wikidata entries'))
    wikimedia_commons_category = models.ForeignKey('WikimediaCommonsCategory', null=True, blank=True, related_name='superlachaise_pois', on_delete=models.SET_NULL, verbose_name=_('wikimedia commons category'))
    main_image = models.ForeignKey('WikimediaCommonsFile', null=True, blank=True, related_name='superlachaise_pois', on_delete=models.SET_NULL, verbose_name=_('main image'))
    superlachaise_categories = models.ManyToManyField('SuperLachaiseCategory', blank=True, related_name='members', through='SuperLachaiseCategoryRelation', verbose_name=_('superlachaise categories'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('date of birth'))
    date_of_death = models.DateField(blank=True, null=True, verbose_name=_('date of death'))
    date_of_birth_accuracy = models.CharField(max_length=255, blank=True, choices=WikidataEntry.accuracy_choices, verbose_name=_('date of birth accuracy'))
    date_of_death_accuracy = models.CharField(max_length=255, blank=True, choices=WikidataEntry.accuracy_choices, verbose_name=_('date of death accuracy'))
    burial_plot_reference = models.CharField(max_length=255, blank=True, verbose_name=_('burial plot reference'))
    
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
    sorting_name = models.CharField(max_length=255, verbose_name=_('sorting name'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseLocalizedPOI, self).save(*args, **kwargs)
        
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
    
    def delete(self):
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
        
        super(SuperLachaiseLocalizedPOI, self).delete()
    
    def __unicode__(self):
        return self.name + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'sorting_name', 'name']
        verbose_name = _('superlachaise localized POI')
        verbose_name_plural = _('superlachaise localized POIs')
        unique_together = ('superlachaise_poi', 'language',)

class SuperLachaiseWikidataRelation(SuperLachaiseModel):
    """ A relation between a Super Lachaise POI and a Wikidata entry """
    
    PERSONS = 'persons'
    ARTISTS = 'artists'
    OTHERS = 'others'
    
    superlachaise_poi = models.ForeignKey('SuperLachaisePOI', verbose_name=_('superlachaise poi'))
    wikidata_entry = models.ForeignKey('WikidataEntry', verbose_name=_('wikidata entry'))
    relation_type = models.CharField(max_length=255, verbose_name=_('relation type'))
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseWikidataRelation, self).save(*args, **kwargs)
        
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
    
    def delete(self):
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
        
        super(SuperLachaiseWikidataRelation, self).delete()
    
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
    
    code = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('code'))
    type = models.CharField(max_length=255, verbose_name=_('type'))
    values = models.CharField(max_length=255, blank=True, verbose_name=_('values'))
    
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
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseLocalizedCategory, self).save(*args, **kwargs)
        
        # Touch SuperLachaise categories
        self.superlachaise_category.save()
    
    def delete(self):
        # Touch SuperLachaise categories
        self.superlachaise_category.save()
        
        super(SuperLachaiseLocalizedCategory, self).delete()
    
    def __unicode__(self):
        return unicode(self.language) + u':' + self.name
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('superlachaise localized category')
        verbose_name_plural = _('superlachaise localized categories')
        unique_together = ('superlachaise_category', 'language',)

class SuperLachaiseCategoryRelation(SuperLachaiseModel):
    """ A relation between a Super Lachaise POI and a SuperLachaise category """
    
    superlachaise_poi = models.ForeignKey('SuperLachaisePOI', verbose_name=_('superlachaise poi'))
    superlachaise_category = models.ForeignKey('SuperLachaiseCategory', verbose_name=_('superlachaise category'))
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseCategoryRelation, self).save(*args, **kwargs)
        
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
    
    def delete(self):
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
        
        super(SuperLachaiseCategoryRelation, self).delete()
    
    def __unicode__(self):
        return unicode(self.superlachaise_poi) + u' - ' + unicode(self.superlachaise_category)
    
    class Meta:
        unique_together = ('superlachaise_poi', 'superlachaise_category',)
        ordering = ['superlachaise_poi', 'superlachaise_category']
        verbose_name = _('superlachaisepoi-superlachaisecategory relationship')
        verbose_name_plural = _('superlachaisepoi-superlachaisecategory relationships')

class WikidataOccupation(SuperLachaiseModel):
    """ Associate a person's occupation to a category """
    
    wikidata_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('wikidata id'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    superlachaise_category = models.ForeignKey('SuperLachaiseCategory', null=True, blank=True, limit_choices_to={'type': SuperLachaiseCategory.OCCUPATION}, related_name='wikidata_occupations', verbose_name=_('superlachaise category'))
    used_in = models.ManyToManyField('WikidataEntry', blank=True, related_name='wikidata_occupations', verbose_name=_('used in'))
    
    def wikidata_url(self, language_code):
        return WikidataEntry.URL_FORMAT.format(id=self.wikidata_id, language_code=language_code)
    
    def __unicode__(self):
        return self.wikidata_id
    
    class Meta:
        ordering = ['wikidata_id']
        verbose_name = _('wikidata occupation')
        verbose_name_plural = _('wikidata occupations')
