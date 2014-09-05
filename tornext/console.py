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
Console logging support.
"""
import sys



class logger(object):

    @staticmethod
    def colorful():
        """
        Returns True if the running system's terminal supports color, and False
        otherwise.
        """
        unsupported_platform = (sys.platform in ('win32', 'Pocket PC'))
        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if unsupported_platform or not is_a_tty:
            return False
        return True


    @staticmethod
    def debug(message, exit=True):
        print '[DEBUG] %s' % message
        if exit is True: sys.exit(1)


    @staticmethod
    def info(message, exit=True):
        print '[INFO] %s' % message
        if exit is True: sys.exit(1)


    @staticmethod
    def warn(message, exit=True):
        print '[WARN] %s' % message
        if exit is True: sys.exit(1)


    @staticmethod
    def error(message, exit=True):
        print '[ERROR] %s' % message
        if exit is True: sys.exit(1)


