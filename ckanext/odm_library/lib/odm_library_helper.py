#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylons
import logging
import json
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

DATASET_TYPE_NAME = 'library_record'

log = logging.getLogger(__name__)

def last_dataset():
  ''' Returns the last dataset info stored in session'''
  if 'last_dataset' in odm_library_helper.session:
    return odm_library_helper.session['last_dataset']

  return None

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return DATASET_TYPE_NAME

session = {}
