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


__all__ = ('add_libs', 'here')


here = lambda base, *dirs: os.path.join(os.path.dirname(os.path.abspath(base)), *dirs)


def add_libs(path):
    """Add libraries into site path from the given path.

    Args:
        path: Thirdparty libraries base path.
    """
    if os.path.exists(path):
        for directory in os.listdir(path):
            lib = os.path.join(path, directory)
            if os.path.isdir(lib) and (lib not in sys.path):
                site.addsitedir(lib)
