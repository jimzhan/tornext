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

from docopt import docopt

from tornext import crypto
from tornext import console
from tornext.utils import Template


basedir = os.path.join(os.path.dirname(__file__), os.path.pardir, 'scaffolds')


logger = console.getLogger()


def execute(args):
    config  = os.path.join('config', 'settings.py')
    project = args['<project>']
    cwd = os.path.join(os.getcwd(), project)
    if os.path.exists(cwd):
        logger.error('%s already exists' % cwd)
    # copy the starter skeleton into current working directory.
    patterns = shutil.ignore_patterns(*('*.css', '*.pyc', 'node_modules'))
    shutil.copytree(os.path.join(basedir, 'project'), cwd, symlinks=False, ignore=patterns)
    shutil.move(os.path.join(cwd, 'project'), os.path.join(cwd, project))
    # create context for created project.
    source = os.path.join(basedir, 'project', 'project', config)
    secret = crypto.generate_cookie_secret()
    with open(os.path.join(cwd, project, config), 'w') as fileobj:
        fileobj.write(Template(source, cookie_secret=secret))


if __name__ == '__main__':
    execute(docopt(__doc__))
