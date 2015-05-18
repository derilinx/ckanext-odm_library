import ckan.plugins as p
import ckan.lib.helpers as h
import plugin as odm_library
from ckan.lib.base import BaseController

class ThemeController(BaseController):
  def library(self):
    return h.redirect_to(controller='package', type='library_record', action='search')
