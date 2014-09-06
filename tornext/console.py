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
"""
Console logging support.
"""
from __future__ import absolute_import

import inspect
import logging

from tornado.log import LogFormatter

from tornext import utils


FORMAT = '%(color)s[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s]%(end_color)s %(message)s'


def getLogger(package=None, level=logging.DEBUG, fmt=FORMAT):
    package = package or utils.traceback(inspect.currentframe()).filename

    logger = logging.getLogger(package)
    stream = logging.StreamHandler()
    stream.setLevel(level)
    stream.setFormatter(LogFormatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S'))
    logger.setLevel(level)
    logger.addHandler(stream)
    return logger
