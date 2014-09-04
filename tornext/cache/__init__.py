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

import hmac
import hashlib
import logging
import functools
try:
    import cPickle as pickle
except ImportError:
    import pickle

from redis.client import Redis

from tornext.sharding import Sharding


logger = logging.getLogger(__name__)


def cache(expires=7200):
    def wrapper(func):
        @functools.wraps(func)
        def function(handler, *args, **kwargs):
            handler.expires = expires
            return func(handler, *args, **kwargs)
        return function
    return wrapper


class AbstractCache(object):

    def get(self, key):
        raise NotImplementedError


    def set(self, key, value, timeout=None):
        raise NotImplementedError


    def delete(self, key):
        raise NotImplementedError


    def exists(self, key):
        raise NotImplementedError



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


class CacheMixin(object):
    """Cache support for `tornado.web.RequestHandler`.
    """
    @property
    def cache(self):
        return self.application.cache


    @property
    def cached_methods(self):
        return 'GET',


    def get_cache_key(self, namespace=None):
        """Generate unique cache key from the incoming request.

        Key components by order:
            namespace: prepare for user identity based caching (None by default).
            user's locale (default: en_US).
            full request url.
        """
        secret  = ''.join((self.request.protocol, '://', self.request.host))
        locale  = self.get_user_locale() or self.get_browser_locale()
        context = [locale.code, self.request.full_url()]
        if namespace:
            context.insert(0, namespace)
        return hmac.new(secret, '|'.join(context), hashlib.sha1).hexdigest()


    def prepare(self):
        super(CacheMixin, self).prepare()
        key = self.get_cache_key()
        if self.cache.exists(key):
            if self.request.method in self.cached_methods:
                data = self.cache.get(key)
                self.write(pickle.loads(data))
                self.finish()


    def write(self, chunk):
        data = pickle.dumps(chunk)
        key  = self.get_cache_key()
        self.cache.set(key, data, getattr(self, 'expires', None))
        super(CacheMixin, self).write(chunk)
