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
"""
from __future__ import with_statement

import random
import string


__all__ = ('generate_cookie_secret',)


def generate_cookie_secret():
    """Generate a random secret key for encrypting cookie.

    Returns: 50 bits random string.
    """
    raw = ''.join([random.SystemRandom().choice("{}{}{}".format(
                    string.ascii_letters,
                    string.digits,
                    string.punctuation)) for i in range(50)])
    return raw.replace("'", "@").replace('"', '#')
