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
from django.apps import apps
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

class AdminCommand(SuperLachaiseModel):
    """ An admin command that can be monitored """
    
    NO_MODIFICATIONS = _("No modifications")
    
    name = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('name'))
    dependency_order = models.IntegerField(null=True, blank=True, verbose_name=_('dependency order'))
    last_executed = models.DateTimeField(blank=True, null=True, verbose_name=_('last executed'))
    last_result = models.TextField(blank=True, null=True, verbose_name=_('last result'))
    
    def perform_command(self):
        call_command(str(self.name))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['dependency_order', 'name']
        verbose_name = _('admin command')
        verbose_name_plural = _('admin commands')

class LocalizedAdminCommand(SuperLachaiseModel):
    """ The part of an Admin Command specific to a language """
    
    language = models.ForeignKey('Language', verbose_name=_('language'))
    admin_command = models.ForeignKey('AdminCommand', related_name='localizations', verbose_name=_('admin command'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    
    def __unicode__(self):
        return unicode(self.admin_command) + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'admin_command']
        verbose_name = _('localized admin command')
        verbose_name_plural = _('localized admin commands')
        unique_together = ('admin_command', 'language',)

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
    
    def __unicode__(self):
        return self.key
    
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
    
    URL_TEMPLATE = u'https://www.openstreetmap.org/{type}/{id}'
    
    NODE = 'node'
    WAY = 'way'
    RELATION = 'relation'
    
    type_choices = (
        (NODE, NODE),
        (WAY, WAY),
        (RELATION, RELATION),
    )
    
    openstreetmap_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('openstreetmap id'))
    type = models.CharField(max_length=255, blank=True, choices=type_choices, verbose_name=_('type'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    sorting_name = models.CharField(max_length=255, blank=True, verbose_name=_('sorting name'))
    nature = models.CharField(max_length=255, blank=True, verbose_name=_('nature'))
    latitude = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=7, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=7, verbose_name=_('longitude'))
    wikidata = models.CharField(max_length=255, blank=True, verbose_name=_('wikidata'))
    wikimedia_commons = models.CharField(max_length=255, blank=True, verbose_name=_('wikimedia commons'))
    
    def openstreetmap_url(self):
        if self.type:
            return OpenStreetMapElement.URL_TEMPLATE.format(type=self.type, id=self.openstreetmap_id)
    
    def wikidata_urls(self, language_code):
        if self.wikidata:
            return [(wikidata, WikidataEntry.URL_TEMPLATE.format(id=wikidata.split(':')[-1], language_code=language_code)) for wikidata in self.wikidata.split(';')]
    
    def wikimedia_commons_url(self):
        if self.wikimedia_commons:
            return WikimediaCommonsCategory.URL_TEMPLATE.format(title=self.wikimedia_commons)
    
    def __unicode__(self):
        return self.openstreetmap_id + u':' + self.name
    
    class Meta:
        ordering = ['sorting_name', 'openstreetmap_id']
        verbose_name = _('openstreetmap element')
        verbose_name_plural = _('openstreetmap elements')

class WikidataEntry(SuperLachaiseModel):
    
    URL_TEMPLATE = u'https://www.wikidata.org/wiki/{id}?userlang={language_code}&uselang={language_code}'
    
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
    
    def wikidata_urls(self, language_code, field):
        if getattr(self, field):
           return [(wikidata, WikidataEntry.URL_TEMPLATE.format(id=wikidata, language_code=language_code)) for wikidata in getattr(self, field).split(';')]
    
    def wikimedia_commons_category_url(self, field):
        if getattr(self, field):
            return WikimediaCommonsCategory.URL_TEMPLATE.format(title=u'Category:%s' % getattr(self, field))
    
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
            return WikipediaPage.URL_TEMPLATE.format(language_code=self.language.code, title=self.wikipedia)
    
    def save(self, *args, **kwargs):
        super(WikidataLocalizedEntry, self).save(*args, **kwargs)
        
        # Touch Wikidata entry
        self.wikidata_entry.save()
    
    def __unicode__(self):
        return self.name + u' (' + unicode(self.language) + u')'
    
    class Meta:
        ordering = ['language', 'name']
        verbose_name = _('wikidata localized entry')
        verbose_name_plural = _('wikidata localized entries')
        unique_together = ('wikidata_entry', 'language',)

class WikipediaPage(SuperLachaiseModel):
    
    URL_TEMPLATE = u'https://{language_code}.wikipedia.org/wiki/{title}'
    
    wikidata_localized_entry = models.OneToOneField('WikidataLocalizedEntry', related_name='wikipedia_page', verbose_name=_('wikidata localized entry'))
    default_sort = models.CharField(max_length=255, blank=True, verbose_name=_('default sort'))
    intro = models.TextField(blank=True, verbose_name=_('intro'))
    
    def save(self, *args, **kwargs):
        # Delete \r added by textfield
        self.intro = self.intro.replace('\r','')
        super(WikipediaPage, self).save(*args, **kwargs)
        
        # Touch Wikidata localized entry
        self.wikidata_localized_entry.save()
    
    def __unicode__(self):
        return self.wikidata_localized_entry.wikipedia + u' (' + unicode(self.wikidata_localized_entry.language) + u')'
    
    class Meta:
        ordering = ['default_sort', 'wikidata_localized_entry']
        verbose_name = _('wikipedia page')
        verbose_name_plural = _('wikipedia pages')

class WikimediaCommonsCategory(SuperLachaiseModel):
    
    URL_TEMPLATE = u'https://commons.wikimedia.org/wiki/{title}'
    
    wikimedia_commons_id = models.CharField(unique=True, db_index=True, max_length=255, verbose_name=_('wikimedia commons id'))
    main_image = models.CharField(max_length=255, blank=True, verbose_name=_('main image'))
    
    def wikimedia_commons_url(self, field):
        if getattr(self, field):
            return WikimediaCommonsCategory.URL_TEMPLATE.format(title=getattr(self, field))
    
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
    
    def wikimedia_commons_url(self, field):
        if getattr(self, field):
            return WikimediaCommonsCategory.URL_TEMPLATE.format(title=getattr(self, field))
    
    def __unicode__(self):
        return self.wikimedia_commons_id
    
    class Meta:
        ordering = ['wikimedia_commons_id']
        verbose_name = _('wikimedia commons file')
        verbose_name_plural = _('wikimedia commons files')

class SuperLachaisePOI(SuperLachaiseModel):
    """ An object linking multiple data sources for representing a single Point Of Interest """
    
    openstreetmap_element = models.OneToOneField('OpenStreetMapElement', unique=True, related_name='superlachaise_poi', verbose_name=_('openstreetmap element'))
    wikidata_entries = models.ManyToManyField('WikidataEntry', related_name='superlachaise_pois', through='SuperLachaiseWikidataRelation', verbose_name=_('wikidata entries'))
    wikimedia_commons_category = models.ForeignKey('WikimediaCommonsCategory', null=True, blank=True, related_name='superlachaise_pois', on_delete=models.SET_NULL, verbose_name=_('wikimedia commons category'))
    main_image = models.ForeignKey('WikimediaCommonsFile', null=True, blank=True, related_name='superlachaise_pois', on_delete=models.SET_NULL, verbose_name=_('main image'))
    superlachaise_categories = models.ManyToManyField('SuperLachaiseCategory', blank=True, related_name='members', through='SuperLachaiseCategoryRelation', verbose_name=_('superlachaise categories'))
    
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
    sorting_name = models.CharField(max_length=255, blank=True, verbose_name=_('sorting name'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('description'))
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseLocalizedPOI, self).save(*args, **kwargs)
        
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['language', 'sorting_name', 'name']
        verbose_name = _('superlachaise localized POI')
        verbose_name_plural = _('superlachaise localized POIs')
        unique_together = ('superlachaise_poi', 'language',)

class SuperLachaiseWikidataRelation(SuperLachaiseModel):
    """ A relation between a Super Lachaise POI and a Wikidata entry """
    
    NONE = 'none'
    PERSON = 'person'
    ARTIST = 'artist'
    
    superlachaise_poi = models.ForeignKey('SuperLachaisePOI', verbose_name=_('superlachaise poi'))
    wikidata_entry = models.ForeignKey('WikidataEntry', verbose_name=_('wikidata entry'))
    relation_type = models.CharField(max_length=255, verbose_name=_('relation type'))
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseWikidataRelation, self).save(*args, **kwargs)
        
        # Touch SuperLachaise POIs
        self.superlachaise_poi.save()
    
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
    
    def save(self, *args, **kwargs):
        super(SuperLachaiseLocalizedCategory, self).save(*args, **kwargs)
        
        # Touch SuperLachaise categories
        self.superlachaise_category.save()
    
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
    
    def __unicode__(self):
        return self.wikidata_id
    
    class Meta:
        ordering = ['wikidata_id']
        verbose_name = _('wikidata occupation')
        verbose_name_plural = _('wikidata occupations')

class PendingModification(SuperLachaiseModel):
    """ A modification to an object that is not yet applied """
    
    CREATE_OR_UPDATE = 'create_or_update'
    DELETE = 'delete'
    
    action_choices = (
        (CREATE_OR_UPDATE, CREATE_OR_UPDATE),
        (DELETE, DELETE),
    )
    
    target_object_class_choices = (
        (AdminCommand.__name__, AdminCommand._meta.verbose_name),
        (LocalizedAdminCommand.__name__, LocalizedAdminCommand._meta.verbose_name),
        (Language.__name__, Language._meta.verbose_name),
        (Setting.__name__, Setting._meta.verbose_name),
        (LocalizedSetting.__name__, LocalizedSetting._meta.verbose_name),
        (SuperLachaiseCategory.__name__, SuperLachaiseCategory._meta.verbose_name),
        (SuperLachaiseLocalizedCategory.__name__, SuperLachaiseLocalizedCategory._meta.verbose_name),
        (WikidataOccupation.__name__, WikidataOccupation._meta.verbose_name),
        (OpenStreetMapElement.__name__, OpenStreetMapElement._meta.verbose_name),
        (WikidataEntry.__name__, WikidataEntry._meta.verbose_name),
        (WikidataLocalizedEntry.__name__, WikidataLocalizedEntry._meta.verbose_name),
        (WikipediaPage.__name__, WikipediaPage._meta.verbose_name),
        (WikimediaCommonsCategory.__name__, WikimediaCommonsCategory._meta.verbose_name),
        (WikimediaCommonsFile.__name__, WikimediaCommonsFile._meta.verbose_name),
        (SuperLachaisePOI.__name__, SuperLachaisePOI._meta.verbose_name),
        (SuperLachaiseWikidataRelation.__name__, SuperLachaiseWikidataRelation._meta.verbose_name),
        (SuperLachaiseCategoryRelation.__name__, SuperLachaiseCategoryRelation._meta.verbose_name),
    )
    
    target_object_class = models.CharField(max_length=255, choices=target_object_class_choices, verbose_name=_('target object class'))
    target_object_id = models.CharField(max_length=255, verbose_name=_('target object id'))
    action = models.CharField(max_length=255, choices=action_choices, verbose_name=_('action'))
    modified_fields = models.TextField(blank=True, verbose_name=_('modified fields'))
    
    def target_object_model(self):
        """ Returns the model class of the target object """
        return apps.get_model(self._meta.app_label, self.target_object_class)
    
    def target_object(self):
        """ Returns the target object """
        target_object_id_dict = json.loads(self.target_object_id)
        return self.target_object_model().objects.filter(**target_object_id_dict).first()
    
    def clean(self):
        if self.target_object_id:
            try:
                target_object_id_dict = json.loads(self.target_object_id) 
            except ValueError as error:
                raise ValidationError({'target_object_id': _('The value must be a JSON dictionary.')})
        
            if not isinstance(target_object_id_dict, dict):
                raise ValidationError({'target_object_id': _('The value must be a JSON dictionary.')})
            
            try:
                invalid_fields = []
                for field in target_object_id_dict:
                    model = self.target_object_model()
                    loop = True
                    for field_part in field.split('__'):
                        if not loop:
                            invalid_fields.append(field)
                            break
                        
                        if not field_part in model._meta.get_all_field_names():
                            invalid_fields.append(field)
                            break
                        
                        # Lookup relations
                        field_type = model._meta.get_field(field_part).get_internal_type()
                        if field_type == 'ForeignKey':
                            model = model._meta.get_field(field_part).rel.to
                        else:
                            loop = False
                
                if invalid_fields:
                    raise ValidationError({'target_object_id': _('The following fields are not fields of the target object model: %s.') % ', '.join(invalid_fields)})
            except LookupError:
                pass
        
        if self.modified_fields:
            try:
                modified_fields_dict = json.loads(self.modified_fields) 
            except ValueError as error:
                raise ValidationError({'modified_fields': _('The value must be a JSON dictionary.')})
        
            if not isinstance(modified_fields_dict, dict):
                raise ValidationError({'modified_fields': _('The value must be a JSON dictionary.')})
            
            try:
                invalid_fields = [field for field in modified_fields_dict if field in ['id', 'pk']]
                if invalid_fields:
                    raise ValidationError({'modified_fields': _('The following fields are not valid: %s.') % ', '.join(invalid_fields)})
                invalid_fields = []
                for field in modified_fields_dict:
                    model = self.target_object_model()
                    loop = True
                    for field_part in field.split('__'):
                        if not loop:
                            invalid_fields.append(field)
                            break
                        
                        if not field_part in model._meta.get_all_field_names():
                            invalid_fields.append(field)
                            break
                        
                        # Lookup relations
                        field_type = model._meta.get_field(field_part).get_internal_type()
                        if field_type == 'ForeignKey':
                            model = model._meta.get_field(field_part).rel.to
                        else:
                            loop = False
                
                if invalid_fields:
                    raise ValidationError({'modified_fields': _('The following fields are not fields of the target object model: %s.') % ', '.join(invalid_fields)})
                
            except LookupError:
                pass
    
    @classmethod
    def resolve_field_relation(cls, object_model, field, value):
        """ Convert a field/value pair to object/value if needed e.g. language__code=fr => language=<Language> """
        if '__' in field:
            resolved_field = field.split('__')[0]
            model = object_model._meta.get_field(resolved_field).rel.to
            resolved_value = model.objects.get(**{'__'.join(field.split('__')[1:]): value})
            result = (resolved_field, resolved_value)
        else:
            # Assert field exists
            object_model._meta.get_field(field)
            result = (field, value)
        return result
    
    def apply_modification(self):
        """ Apply the modification and delete self """
        self.full_clean()
        if self.action == PendingModification.CREATE_OR_UPDATE:
            # Get or create target object
            target_object_model = self.target_object_model()
            target_object_id_dict = {field:value for (field, value) in [self.resolve_field_relation(target_object_model, field, value) for (field, value) in json.loads(self.target_object_id).iteritems()]}
            target_object, created = target_object_model.objects.get_or_create(**target_object_id_dict)
            
            # Apply field modifications
            if self.modified_fields:
                modified_fields_dict = {field:value for (field, value) in [self.resolve_field_relation(target_object_model, field, value) for (field, value) in json.loads(self.modified_fields).iteritems()]}
                for field, value in modified_fields_dict.iteritems():
                    field_type = target_object_model._meta.get_field(field).get_internal_type()
                    if field_type == 'CharField' and value == None:
                        setattr(target_object, field, u'')
                    else:
                        setattr(target_object, field, value)
            
            target_object.save()
        elif self.action == PendingModification.DELETE:
            # Delete target object
            self.target_object().delete()
        
        # Delete pending modification
        if self.pk:
            self.delete()
    
    def __unicode__(self):
        try:
            target_object = self.target_object()
            if target_object:
                return self.action + u': ' + unicode(self.target_object())
        except:
            pass
        return self.action
    
    class Meta:
        ordering = ['action', 'target_object_class', 'target_object_id']
        verbose_name = _('pending modification')
        verbose_name_plural = _('pending modifications')
        unique_together = ('target_object_class', 'target_object_id',)
