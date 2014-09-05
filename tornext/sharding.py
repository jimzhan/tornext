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
 consistent hashing for nosql client
 based on ezmobius client (redis-rb)
 and see this article http://amix.dk/blog/viewEntry/19367

ref: https://github.com/Doist/hash_ring
"""
from __future__ import absolute_import

import zlib
import bisect

from tornext import consts


class Sharding(object):
    """Consistent hash for nosql API"""
    def __init__(self, nodes=[], replicas=128):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        """
        self.nodes = set()
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

        for n in nodes:
            self.add_node(n)

    def add_node(self, node):
        """Adds a `node` to the hash ring (including a number of replicas).
        """
        self.nodes.add(node)
        for x in consts.xrange(self.replicas):
            crckey = zlib.crc32(consts.Byte("%s:%d" % (node, x)))
            self.ring[crckey] = node
            self.sorted_keys.append(crckey)

        self.sorted_keys.sort()

    def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        self.nodes.remove(node)
        for x in consts.xrange(self.replicas):
            crckey = zlib.crc32(consts.Byte("%s:%d" % (node, x)))
            self.ring.remove(crckey)
            self.sorted_keys.remove(crckey)

    def get_node(self, key):
        """Given a string key a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        n, i = self.get_node_pos(key)
        return n

    def get_node_pos(self, key):
        """Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if len(self.ring) == 0:
            return [None, None]
        crc = zlib.crc32(consts.Byte(key))
        idx = bisect.bisect(self.sorted_keys, crc)
        idx = min(idx, (self.replicas * len(self.nodes)) - 1)
        # prevents out of range index
        return [self.ring[self.sorted_keys[idx]], idx]

    def iter_nodes(self, key):
        """Given a string key it returns the nodes as a generator that can hold the key.
        """
        if len(self.ring) == 0:
            yield None, None
        node, pos = self.get_node_pos(key)
        for k in self.sorted_keys[pos:]:
            yield k, self.ring[k]

    def __call__(self, key):
        return self.get_node(key)
