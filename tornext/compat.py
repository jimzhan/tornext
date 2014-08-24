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
Unified constants with cross-version (2.0 - 3.0) supports.
----------------------------

The constants defined in this module are:

.. data:: cwd

    Current working directory of the script, default is :data:`os.path.curdir`.
    By changing this value, all consequent :mod:`sirocco.core.system` operations
    will be running under the updated value.


.. data:: UnicodeType

    Generic unicode type which support python 2 ~ 3.


.. data:: StringType

    Generic string type which support python 2 ~ 3.


.. data:: RegexType

    Compiled :mod:`re` pattern type.


.. data:: maxint

    Maximum integer current system support, provided by :data:`sys.maxsize` in python 3,
    under python 2, the value is provied by :data:`sys.maxint`.

"""
from __future__ import absolute_import

import sys
import types
import codecs


IsPy3   = (sys.version_info.major == 3)


#==========================================================================================
#   Removed Types@Python3
#==========================================================================================
UnicodeType = IsPy3 and str or getattr(types, 'UnicodeType')
StringType  = IsPy3 and str or getattr(types, 'StringTypes')


#==========================================================================================
#   Self-Adaptive Constants for both Python2 and Python3
#==========================================================================================
maxint = IsPy3 and getattr(sys, 'maxsize') or getattr(sys, 'maxint')


#==========================================================================================
#   Self-Adaptive lambdas for both Python2 and Python3
#==========================================================================================
if IsPy3:
    xrange    = range

    Byte      = lambda data: isinstance(data, bytes) and data or codecs.latin_1_encode(data)[0]
    ByteIndex = lambda data, idx: data[idx]
    IterBytes = lambda data: iter(data)
else:
    xrange    = xrange

    Byte      = lambda data: data
    ByteIndex = lambda data, idx: ord(data[idx])
    IterBytes = lambda data: (ord (char) for char in data)
