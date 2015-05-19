import ckan
import pylons
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_library_helper
import datetime
import time
from urlparse import urlparse
import json
import collections

log = logging.getLogger(__name__)

def library_fields():
  '''Return a list of library fields'''

  log.debug('library_fields')

  return odm_library_helper.library_fields

class OdmLibraryPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong library plugin.'''

  plugins.implements(plugins.IDatasetForm)
  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IFacets)

  def dataset_facets(self, facets_dict, package_type):

    facets_dict = {
              'license_id': toolkit._('License'),
              'organization': toolkit._('Organizations'),
              'groups': toolkit._('Groups'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):

    group_facets = {
              'license_id': toolkit._('License'),
              'organization': toolkit._('Organizations'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return group_facets

  def organization_facets(self, facets_dict, organization_type, package_type):

    organization_facets = {
              'license_id': toolkit._('License'),
              'groups': toolkit._('Groups'),
              'tags': toolkit._('Tags'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return organization_facets

  def before_map(self, m):

    m.connect('library', #name of path route
      '/library', #url to map path to
      controller='ckanext.odm_library.controller:ThemeController',action='library')

    return m

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'odm_library')
    toolkit.add_public_directory(config, 'public')

  def get_helpers(self):
    '''Register the plugin's functions above as a template helper function.'''

    return {
      'odm_library_library_fields': library_fields
    }

  def _modify_package_schema_write(self, schema):

    for library_field in odm_library_helper.library_fields:
      validators_and_converters = [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_extras'), ]
      if library_field[2]:
        validators_and_converters.insert(1,validate_not_empty)
      schema.update({library_field[0]: validators_and_converters})

    for tag_dictionary in odm_library_helper.tag_dictionaries:
      schema.update({tag_dictionary[0]: [toolkit.get_validator('ignore_missing'),toolkit.get_converter('convert_to_tags')(tag_dictionary[0])]})

    return schema

  def _modify_package_schema_read(self, schema):

    for library_field in odm_library_helper.library_fields:
      validators_and_converters = [toolkit.get_converter('convert_from_extras'),toolkit.get_validator('ignore_missing')]
      if library_field[2]:
        validators_and_converters.append(validate_not_empty)
      schema.update({library_field[0]: validators_and_converters})

    for tag_dictionary in odm_library_helper.tag_dictionaries:
      schema.update({tag_dictionary[0]: [toolkit.get_converter('convert_from_tags')(tag_dictionary[0]),toolkit.get_validator('ignore_missing')]})

    return schema

  def create_package_schema(self):
    schema = super(OdmLibraryPlugin, self).create_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def update_package_schema(self):
    schema = super(OdmLibraryPlugin, self).update_package_schema()
    schema = self._modify_package_schema_write(schema)
    return schema

  def show_package_schema(self):
    schema = super(OdmLibraryPlugin, self).show_package_schema()
    schema = self._modify_package_schema_read(schema)
    return schema

  def is_fallback(self):
    return False

  def package_types(self):
    return ["library_record"]
