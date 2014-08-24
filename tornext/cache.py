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

from redis.client import Redis

#from tornado.options import options

#from tornext import utils
from tornext.sharding import Sharding


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
    """
    Default sharding settings for single node (direct settings for `redis.client.StrictRedis`).
    {
        'host': 'localhost', 'port': 6379,
        'db': 0, 'password': None, 'socket_timeout': None,
        'socket_connect_timeout': None,
        'socket_keepalive': None, 'socket_keepalive_options': None,
        'connection_pool': None, 'unix_socket_path': None,
        'encoding': 'utf-8', 'encoding_errors': 'strict',
        'charset': None, 'errors': None,
        'decode_responses': False, 'retry_on_timeout': False,
        'ssl': False, 'ssl_keyfile': None, 'ssl_certfile': None,
        'ssl_cert_reqs': None, 'ssl_ca_certs': None
    }

    """
    def __init__(self, nodes, **settings):
        """
        Args:
            nodes: list of connection urls for `redis.client.StrictRedis#from_url`.
            settings: additional settings for redis client.

        Attributes:
            mapping (dict): maintain the connection url & corresponding Redis client mapping.
            dispather: `tornext.sharding.Sharding` instance for dispatching requests.
        """
        self.dispatcher = Sharding(nodes)
        self.mapping = dict([(url, Redis.from_url(url)) for url in nodes])


    def get_node(self, key):
        """Get the corresponding sharding node for the given key.

        Args:
            key (str): md5-based cache key.

        Returns:
            instance of `redis.client.Redis` for accessing single Redis node.
        """
        return self.dispatcher.get_node(key)
