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
import logging

from redis.client import Redis

from tornext.sharding import Sharding
from tornext.cache import AbstractCache


logger = logging.getLogger(__name__)


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
    def __init__(self, urls, **settings):
        """
        Args:
            urls: list of connection urls for `redis.client.StrictRedis#from_url`.
            settings: additional settings for redis client.

        Attributes:
            mapping (dict): maintain the connection url & corresponding Redis client mapping.
            sharding: `tornext.sharding.Sharding` instance for dispatching requests.
        """
        self.sharding = Sharding(urls)
        self.mapping  = dict([(url, Redis.from_url(url)) for url in urls])


    def get_node(self, key):
        """Get the corresponding sharding node for the given key.

        Args:
            key (str): md5-based cache key.

        Returns:
            instance of `redis.client.Redis` for accessing single Redis node.
        """
        url = self.sharding.get_node(key)
        return self.mapping.get(url)


    def exists(self, key):
        """Check if `key` exists.

        Args:
            key: hex-digested cache key.

        Returns: boolean value indicating if corresponding `key` exists.
        """
        node = self.get_node(key)
        return node and node.exists(key) or False


    def get(self, key):
        """Get cached item via the md5 key.

        Fetch the corresponding sharding node for consequent requests.

        Args:
            key: md5-based cache key.

        Returns: value for `key` at sharding node, or None if the key doesn't exist.
        """
        node = self.get_node(key)
        return node and node.get(key) or None


    def set(self, key, value, timeout=None):
        """Set the value for key.

        Args:
            key: md5-based cache key.
            value: value to be set.
            timeout: expire the value in a given period (seconds).
        """
        node = self.get_node(key)
        node.set(key, value, isinstance(timeout, int) and timeout or None)


    def delete(self, *keys):
        """Delete cached items with given keys.

        Args:
            keys: single cache key or list of cache keys.
        """
        if isinstance(keys, (tuple, list)):
            for key in keys:
                node = self.get_node(key)
                node.delete(key)
        else:
            node = self.get_node(key)
            node.delete(key)


