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
from pylons import config
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
	plugins.implements(plugins.IPackageController, inherit=True)

	def __init__(self, *args, **kwargs):

		log.debug('OdmLibraryPlugin init')
		wsgi_app = SessionMiddleware(None, None)
		odm_library_helper.session = wsgi_app.session

	def before_map(self, m):

		m.connect('odm_library_index','/library_record',controller='package',type='library_record',action='search')

		m.connect('odm_library_new','/library_record/new',controller='package',type='library_record',action='new')

		m.connect('odm_library_new_resource','/library_record/new_resource/{id}',controller='package',type='library_record',action='new_resource')

		m.connect('odm_library_read', '/library_record/{id}',controller='package',type='library_record', action='read', ckan_icon='book')

		m.connect('odm_library_edit', '/library_record/edit/{id}',controller='package',type='library_record', action='edit')

		m.connect('odm_library_delete', '/library_record/delete/{id}',controller='package',type='library_record', action='delete')

		return m

	def update_config(self, config):
		'''Update plugin config'''

		toolkit.add_template_directory(config, 'templates')
		toolkit.add_resource('fanstatic', 'odm_library')
		toolkit.add_public_directory(config, 'public')

	def get_helpers(self):
		'''Register the plugin's functions above as a template helper function.'''

		return {
			'odm_library_get_dataset_type': odm_library_helper.get_dataset_type,
			'odm_library_validate_fields': odm_library_helper.validate_fields
		}

	def after_create(self, context, pkg_dict):

		dataset_type = context['package'].type if 'package' in context else pkg_dict['type']

		if dataset_type == 'library_record':
			log.debug('after_create: %s', pkg_dict['name'])

			# Create default Issue
			review_system = toolkit.asbool(config.get("ckanext.issues.review_system", False))
			if review_system:
				if pkg_dict['type'] == 'library_record':
					odm_library_helper.create_default_issue_library_record(pkg_dict)
