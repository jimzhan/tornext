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
from tornado.util import ObjectDict
from tornado.options import (define,
                            options,
                            parse_config_file)


########################################
# Default Tornado Application Settings #
########################################
# general settings #
####################
define('debug', default=True, group='app', help='Application debug flag')
define('compress_response', default=not options.debug, group='app')
define('default_handler_class', group='app')
define('default_handler_args',  group='app')
#define('ui_modules', default={}, group='app')
#define('ui_methods', group='app')
# outside the application scope
define('port',   default=8000,  help="run on the given port")
define('config', callback=lambda path: parse_config_file(path, final=False))
#################
# auth settings #
#################
define('cookie_secret', group='app')
define('login_url',     default='/login', group='app')
define('xsrf_cookies',  default=True,  group='app')
######################
# templates settings #
######################
define('autoescape', default='xhtml_escape', group='app')
define('template_path', group='app')
#########################
# static files settings #
#########################
define('static_path', type=str, group='app')
define('static_url_prefix', default='/assets/', group='app')
define('static_hash_cache', default=True, group='app')


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
