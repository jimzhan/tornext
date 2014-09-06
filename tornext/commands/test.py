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
Usage: tornext test [options]

Options:
    -h, --help          show this help message and exit.

See 'tornext help <command>' for more information on a specific command.
"""
from __future__ import with_statement

import os
import tornext

from docopt import docopt
from subprocess import call


basedir = os.path.join(os.path.dirname(tornext.__file__), 'tests')


def execute(args):
    exit(call(['python', os.path.join(basedir, 'runtests.py')]))


if __name__ == '__main__':
    execute(docopt(__doc__))
