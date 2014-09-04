#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 Jim Zhan <jim.zhan@me.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
"""
[Ref](http://tornado.readthedocs.org/en/latest/web.html#tornado.web.Application.settings)

Default all available settings via `tornado.options.options`
for config file, as the options in config file will not be
available until they are defined via `tornado.options.define`
beforehand.
"""
from tornado.options import define, options, parse_config_file
from tornado.util import ObjectDict


########################################
# Default Tornado Application Settings #
########################################
# general settings #
####################
define('debug', default=True, group='application', help='Application debug flag')
define('compress_response', default=not options.debug, group='application')
define('default_handler_class', group='application')
define('default_handler_args',  group='application')
define('ui_modules', group='application')
define('ui_methods', group='application')
# outside the application scope
define('root',   type=str, help='application root dir')
define('port',   default=8000,  help="run on the given port")
define('config', callback=lambda path: parse_config_file(path, final=False))
#################
# auth settings #
#################
define('cookie_secret', group='application')
define('login_url',     default='/login', group='application')
define('xsrf_cookies',  default=True,  group='application')
######################
# templates settings #
######################
define('autoescape', default='xhtml_escape', group='application')
define('template_path', group='application')
#########################
# static files settings #
#########################
define('static_path', type=str, group='application')
define('static_url_prefix', default='/assets/', group='application')
define('static_hash_cache', default=True, group='application')


################################
# Default Application Settings #
################################
# Cache Settings #
##################
define('cache', default=ObjectDict())
#####################
# Database Settings #
#####################
define('database', default=ObjectDict())
###########################
# Other Services Settings #
###########################
define('service', default=ObjectDict())
