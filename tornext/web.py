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

import logging

from tornado import web
from tornado import ioloop
from tornado.options import options


logger = logging.getLogger(__name__)


class Application(web.Application):
    """Extension for `tornado.web.Application` with config support.
    """
    def __init__(self, handlers, config='settings.py', **kwargs):
        # trigger parse_config_file
        options.config = config
        settings = options.group_dict('app')
        settings.update(kwargs)
        super(Application, self).__init__(handlers,**settings)


    def start(self, port, address='127.0.0.1', **settings):
        """Starts an HTTP server for this application on the given port.
        """
        # import is here rather than top level because HTTPServer
        # is not importable on appengine
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self, **settings)
        server.listen(port, address=address)
        ioloop.IOLoop.instance().start()
