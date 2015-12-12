# -*- coding: utf-8 -*-

"""
urls.py
superlachaise_api

Created by Maxime Le Moine on 05/06/2015.
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

from django.conf.urls import patterns, url

from superlachaise_api import views

urlpatterns = [
    url(r'^licence/$', views.licence),
    
    url(r'^openstreetmap_elements/$', views.openstreetmap_element_list),
    url(r'^openstreetmap_elements/(?P<type>[^\/]*)/$', views.openstreetmap_element_list),
    url(r'^openstreetmap_elements/(?P<type>[^\/]*)/(?P<id>[0-9]*)/$', views.openstreetmap_element),
    
    url(r'^wikidata_entries/$', views.wikidata_entry_list),
    url(r'^wikidata_entries/(?P<id>Q[0-9]*)/$', views.wikidata_entry),
    
    url(r'^wikimedia_commons_categories/$', views.wikimedia_commons_category_list),
    url(r'^wikimedia_commons_categories/(?P<id>[^\/]*)/$', views.wikimedia_commons_category),
    
    url(r'^superlachaise_categories/$', views.superlachaise_category_list),
    url(r'^superlachaise_categories/(?P<id>[^\/]*)/$', views.superlachaise_category),
    
    url(r'^superlachaise_pois/$', views.superlachaise_poi_list),
    url(r'^superlachaise_pois/(?P<id>[0-9]*)/$', views.superlachaise_poi),
    url(r'^superlachaise_pois/(?P<superlachaisepoi_id>[0-9]*)/openstreetmap_element/$', views.openstreetmap_element),
    url(r'^superlachaise_pois/(?P<superlachaisepoi_id>[0-9]*)/wikimedia_commons_category/$', views.wikimedia_commons_category),
    url(r'^superlachaise_pois/(?P<superlachaisepoi_id>[0-9]*)/superlachaise_categories/$', views.superlachaise_category_list),
    url(r'^superlachaise_pois/(?P<superlachaisepoi_id>[0-9]*)/wikidata_entries/(?P<relation_type>[^\/]*)/$', views.wikidata_entry_list),
    
    url(r'^$', views.objects),
]
