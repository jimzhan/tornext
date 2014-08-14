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

import os
import sys
import site


__all__ = ('add_libs',)


def add_libs(basedir):
    """Add libraries into site path from the given path.

    Args:
        basedir: Thirdparty libraries base path.
    """
    if os.path.exists(basedir):
        for directory in os.listdir(basedir):
            lib = os.path.join(basedir, directory)
            if os.path.isdir(lib) and (lib not in sys.path):
                site.addsitedir(lib)
