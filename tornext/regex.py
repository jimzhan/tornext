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
Regular expression helpers & constants.
"""
import re
from tornext import consts

######################################################################
#  Regular Expression patterns
######################################################################
email   = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)

date    = re.compile(r'^(19[0-9][0-9]|20[0-9][0-9])(-)(0?[1-9]|1[0-2])(-)(0?[1-9]|[12][0-9]|3[01])$')
time    = re.compile(r'^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$')
datetime= re.compile(r'^(19[0-9][0-9]|20[0-9][0-9])(-)(0?[1-9]|1[0-2])(-)(0?[1-9]|[12][0-9]|3[01])'
        '\s(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$')

ip      = re.compile(r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
uuid    = re.compile(r'^(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$')

md5     = re.compile(r'^\w{32}$')
sha1    = re.compile(r'^\w{40}$')
sha256  = re.compile(r'^\w{64}$')


class url:
    patterns = [
        re.compile("""([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]"""),
        re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?"),
        re.compile("(~/|/|\\./)([-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]|\\\\)+"),
        #re.compile("'\\<((mailto:)|)[-A-Za-z0-9\\.]+@[-A-Za-z0-9\\.]+"),
    ]

    @classmethod
    def match(cls, value):
        return cls.patterns[0].match(value) \
                or cls.patterns[1].match(value) \
                or cls.patterns[2].match(value)

    @classmethod
    def search(cls, value):
        return cls.patterns[0].match(value) \
                or cls.patterns[1].search(value) \
                or cls.patterns[2].search(value)


#============================== common ==============================
def is_regex(pattern):
    """
    Check if `pattern` compiled :mod:`re` pattern.

    Args:
        * pattern: object to check.

    Returns:
        :data:`True` if :data:`pattern` is a compiled :mod:`re` expression, :data:`False` otherwise.
    """
    return type(pattern) is consts.RegexType

