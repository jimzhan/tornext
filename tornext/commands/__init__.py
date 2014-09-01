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
import os
import os.path
import sys
import argparse


here = os.path.abspath(os.path.dirname(__file__))


def find_commands():
    """Find a list of available commands.

    Returns: Available command list.
    """
    try:
        return [item[:-3] for item in os.listdir(here)
                if not item.startswith('_') and item.endswith('.py')]
    except OSError:
        return []



class AbstractCommand(object):

    def execute(self, *args, **kwargs):
        raise NotImplementedError


    @property
    def message(self):
        raise NotImplementedError



class OptionParser(argparse.ArgumentParser):
    pass
