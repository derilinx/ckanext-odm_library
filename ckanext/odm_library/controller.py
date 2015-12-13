import ckan.plugins as p
import logging
import sys
import os
import ckan.lib.helpers as h
import plugin as odm_library
from ckan.lib.base import BaseController, render
import ckan.model as model
from ckan.common import c, request
from ckan.controllers.package import PackageController
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_library_helper

log = logging.getLogger(__name__)

class LibraryController(PackageController):

  def new(self, data=None, errors=None, error_summary=None):

    log.debug('LibraryController new')

    return super(LibraryController, self).new(data=data, errors=errors,error_summary=error_summary)

  def search(self):

    log.debug('LibraryController search')

    return super(LibraryController, self).search()

  def read(self, id, format='html'):

    log.debug('LibraryController read')

    return super(LibraryController, self).read(id=id,format=format)

  def edit(self, id, data=None, errors=None, error_summary=None):

    log.debug('LibraryController edit')

    return super(LibraryController, self).edit(id, data=data, errors=errors,error_summary=error_summary)

  def delete(self, id):

    log.debug('LibraryController delete')

    return super(LibraryController, self).delete(id)

  def new_resource(self, id, data=None, errors=None, error_summary=None):

    log.debug('LibraryController new_resource')

    return super(LibraryController, self).new_resource(id, data=data, errors=errors, error_summary=error_summary)

  def _guess_package_type(self, expecting_name=False):

    log.debug('LibraryController _guess_package_type')

    return odm_library_helper.get_dataset_type()
