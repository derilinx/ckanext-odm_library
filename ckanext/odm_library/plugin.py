import ckan
import pylons
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from beaker.middleware import SessionMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_library_helper
from urlparse import urlparse
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

class OdmLibraryPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong library plugin.'''

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IFacets)
  plugins.implements(plugins.IPackageController, inherit=True)

  def __init__(self, *args, **kwargs):

    log.debug('OdmLibraryPlugin init')
    wsgi_app = SessionMiddleware(None, None)
    odm_library_helper.session = wsgi_app.session

  def dataset_facets(self, facets_dict, package_type):

    facets_dict = {
              'license_id': toolkit._('License'),
              'tags': toolkit._('Topics'),
              'organization': toolkit._('Organizations'),
              'groups': toolkit._('Groups'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):

    group_facets = {
              'license_id': toolkit._('License'),
              'tags': toolkit._('Topics'),
              'organization': toolkit._('Organizations'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return group_facets

  def organization_facets(self, facets_dict, organization_type, package_type):

    organization_facets = {
              'license_id': toolkit._('License'),
              'tags': toolkit._('Topics'),
              'groups': toolkit._('Groups'),
              'res_format': toolkit._('Formats'),
              'odm_language': toolkit._('Language'),
              'odm_spatial_range': toolkit._('Country')
              }

    return organization_facets

  def before_map(self, m):

    m.connect('odm_library_index','/library',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='search')

    m.connect('odm_library_new','/library/new',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='new')

    m.connect('odm_library_new_resource','/library/new_resource/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record',action='new_resource')

    m.connect('odm_library_read', '/library/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record', action='read', ckan_icon='book')

    m.connect('odm_library_edit', '/library/edit/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record', action='edit')

    m.connect('odm_library_delete', '/library/delete/{id}',
      controller='ckanext.odm_library.controller:LibraryController',type='library_record', action='delete')

    return m

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'odm_library')
    toolkit.add_public_directory(config, 'public')

  def get_helpers(self):
    '''Register the plugin's functions above as a template helper function.'''

    return {
      'odm_library_last_dataset': odm_library_helper.last_dataset,
      'odm_library_get_dataset_type': odm_library_helper.get_dataset_type
    }

  def is_fallback(self):
    return False

  def package_types(self):
    return [odm_library_helper.get_dataset_type()]

  def new_template(self):
    return 'library/new.html'

  def read_template(self):
    return 'library/read.html'

  def edit_template(self):
    return 'library/edit.html'

  def search_template(self):
    return 'library/search.html'

  def package_form(self):
    return 'library/new_package_form.html'

  def resource_form(self):
    return 'library/snippets/resource_form.html'

  def before_create(self, context, resource):
    log.info('before_create')

    odm_library_helper.session['last_dataset'] = None
    odm_library_helper.session.save()

  def after_create(self, context, pkg_dict):
    log.debug('after_create: %s', pkg_dict['name'])

    odm_library_helper.session['last_dataset'] = pkg_dict
    odm_library_helper.session.save()

  def after_update(self, context, pkg_dict):
    log.debug('after_update: %s', pkg_dict['name'])

    odm_library_helper.session['last_dataset'] = pkg_dict
    odm_library_helper.session.save()
