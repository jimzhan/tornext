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
Python 2/3 self-adaptors.
"""
from __future__ import absolute_import

import re
import sys
import types
import codecs


IsPy3   = (sys.version_info.major == 3)

#==========================================================================================
#   Types
#==========================================================================================
UnicodeType = IsPy3 and str or getattr(types, 'UnicodeType')
StringType  = IsPy3 and str or getattr(types, 'StringTypes')
RegexType   = type(re.compile(r'RegexType'))


#==========================================================================================
#   Constants
#==========================================================================================
maxint = IsPy3 and getattr(sys, 'maxsize') or getattr(sys, 'maxint')


#==========================================================================================
#   Attributes
#==========================================================================================
if IsPy3:
    _meth_func = "__func__"
    _meth_self = "__self__"

    _func_closure = "__closure__"
    _func_code = "__code__"
    _func_defaults = "__defaults__"
    _func_globals = "__globals__"

    _iterkeys = "keys"
    _itervalues = "values"
    _iteritems = "items"
    _iterlists = "lists"

    xrange    = range

    Byte      = lambda data: isinstance(data, bytes) and data or codecs.latin_1_encode(data)[0]
    ByteIndex = lambda data, idx: data[idx]
    IterBytes = lambda data: iter(data)
else:
    _meth_func = "im_func"
    _meth_self = "im_self"

    _func_closure = "func_closure"
    _func_code = "func_code"
    _func_defaults = "func_defaults"
    _func_globals = "func_globals"

    _iterkeys = "iterkeys"
    _itervalues = "itervalues"
    _iteritems = "iteritems"
    _iterlists = "iterlists"

    xrange    = xrange

    Byte      = lambda data: data
    ByteIndex = lambda data, idx: ord(data[idx])
    IterBytes = lambda data: (ord (char) for char in data)


def iterkeys(d, **kw):
    """Return an iterator over the keys of a dictionary."""
    return iter(getattr(d, _iterkeys)(**kw))


def itervalues(d, **kw):
    """Return an iterator over the values of a dictionary."""
    return iter(getattr(d, _itervalues)(**kw))


def iteritems(d, **kw):
    """Return an iterator over the (key, value) pairs of a dictionary."""
    return iter(getattr(d, _iteritems)(**kw))
