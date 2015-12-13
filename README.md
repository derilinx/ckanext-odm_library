ckanext-odm_library
=================

[![Build Status](https://travis-ci.org/OpenDevelopmentMekong/ckanext-odm_library.svg?branch=master)](https://travis-ci.org/OpenDevelopmentMekong/odm_library)

A CKAN extension which provides with template files and logic to implement OD Mekong's library

# Installation

In order to install this CKAN Extension:

  * clone the ckanext-odm_library folder to the src/ folder in the target CKAN instance.

 ```
 git clone https://github.com/OpenDevelopmentMekong/ckanext-odm_library.git
 cd ckanext-odm_library
 ```

 * Install dependencies
 <code>pip install -r requirements.txt</code>

 * Setup plugin
 <code>python setup.py develop</code>

# This theme uses ckanext-scheming and ckanext-fluent

In order for this theme to function properly, following CKAN extensions need to be installed:

ckanext-scheming: https://github.com/ckan/ckanext-scheming
ckanext-fluent: https://github.com/ckan/ckanext-fluent

and following variables added to the ckan config file (development.ini/production.ini):

```
scheming.dataset_schemas = ckanext.odm_library:odm_library_schema.json
scheming.presets = ckanext.odm_library:odm_presets.json
                  ckanext.fluent:presets.json
scheming.dataset_fallback = false

```

# Testing

  TBD

# Copyright and License

This material is copyright (c) 2014-2015 East-West Management Institute, Inc. (EWMI).

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0 whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
