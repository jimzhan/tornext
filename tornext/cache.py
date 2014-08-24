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
Redis-based cache helpers.
"""
from __future__ import absolute_import

import logging

from tornado.options import options
from tornext import utils


logger = logging.getLogger(__name__)


class AbstractCache(object):

    def clear(self):
        raise NotImplementedError


    def delete(self, key):
        raise NotImplementedError


    def get(self, key):
        raise NotImplementedError


    def set(self, key, value, timeout=None, **options):
        raise NotImplementedError



class MemoryCache(AbstractCache):
    pass


class RedisCache(AbstractCache):
    pass

