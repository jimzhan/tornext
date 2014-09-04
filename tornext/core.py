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

"""
import os
import sys
import yaml
import inspect
import logging

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from tornado import web
from tornado import ioloop
from tornado.util import exec_in
from tornado.options import define, options

from tornext import debug
from tornext import settings


logger = logging.getLogger(__name__)


def load_user_settings(config):
    """Fetch user's settings & merge with defaults (`tornext.settings`).

    Args:
        config: user's settings file path (YAML).

    Returns: `dict` merged with `tornado.settings` & user's YAML.
    """
    if os.path.exists(config) and os.path.isfile(config):
        user_settings = yaml.load(file(config, 'r'), Loader=Loader)
        settings.update(user_settings.get('tornado', {}))
    return settings


def configure(config):
    """Fetch user's settings & merge with defaults (`tornext.settings`).

    Args:
        config: Python-based user's settings file path.
    """

    if os.path.exists(config) and os.path.isfile(config):
        pass



class Application(web.Application):
    """Extension for `tornado.web.Application` with config support.
    """
    def __init__(self, handlers, default_host="", transforms=None, config='app.yml'):
        super(Application, self).__init__(handlers,
                                        default_host,
                                        transforms,
                                        **load_user_settings(config))


    def start(self, port, **settings):
        """Starts an HTTP server for this application on the given port.
        """
        if not hasattr(options, 'basedir'):
            traceback = debug.traceback(inspect.currentframe())
            basedir = os.path.abspath(os.path.dirname(traceback.filename))
            define('basedir', default=basedir, help='Base directory of the project.')
        # import is here rather than top level because HTTPServer
        # is not importable on appengine
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self, **settings)
        server.listen(port, address='127.0.0.1')
        ioloop.IOLoop.instance().start()
