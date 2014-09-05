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
Usage: tornext create <project> [options]

Arguments:
    project             project name to be created under current working directory.

Options:
    -h, --help          show this help message and exit.

See 'tornext help <command>' for more information on a specific command.
"""
from __future__ import with_statement

import os
import shutil
import tornext
from docopt import docopt

from tornext import crypto
from tornext.console import logger
from tornext.utils import Template


Scaffolds = os.path.join(os.path.dirname(tornext.__file__), 'scaffolds')


def execute(args):
    cwd = os.path.join(os.getcwd(), args['<project>'])
    if os.path.exists(cwd):
        logger.error('%s already exists' % cwd)
    # copy the starter skeleton into current working directory.
    template = os.path.join(Scaffolds, 'starter')
    patterns = shutil.ignore_patterns(*('*.css', '*.js', '*.pyc', 'node_modules'))
    shutil.copytree(template, cwd, symlinks=False, ignore=patterns)
    # create context for created project.
    source = os.path.join(Scaffolds, 'settings.py')
    secret = crypto.generate_cookie_secret()
    with open(os.path.join(cwd, 'settings.py'), 'w') as fileobj:
        fileobj.write(Template(source, cookie_secret=secret))


if __name__ == '__main__':
    execute(docopt(__doc__))
