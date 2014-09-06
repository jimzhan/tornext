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

import re
import os.path

from docopt import docopt
from subprocess import call


class Manager(object):

    basedir = os.path.dirname(__file__)

    def __init__(self, docstring, **kwargs):
        self.args = docopt(docstring, **kwargs)
        self.argv = [self.args['<command>']] + self.args['<args>']
        self.cmd  = self.args['<command>']


    @property
    def commands(self):
        """Find all available management commands.

        Returns: list of commands under `tornext.commands`.
        """
        pattern = re.compile(r'^([a-zA-Z]+)(\w?)(\.py)')
        return [py[:-3] for py in os.listdir(self.basedir) if pattern.match(py)]


    def dispatch(self):
        """Dynamically dispatch the given command to concrete python script.
        """
        if self.cmd in self.commands:
            py = os.path.join(self.basedir, '%s.py' % self.cmd)
            exit(call(['python', py] + self.argv))


