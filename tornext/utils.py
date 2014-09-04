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
from __future__ import absolute_import, with_statement

import os
import sys
import site
import string
import inspect
import logging

from functools import wraps
from timeit import default_timer as timer


__all__ = ('add_libs', 'Template', 'timeit', 'traceback', 'here')


logger = logging.getLogger(__name__)


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


def Template(path, **context):
    """Simple file-based template shortcut.

    Using built-in `string.Template` with `safe_substitute` method.

    Args:
        path: template file path.

    Returns: substituted file content.
    """
    with open(path, 'r') as fileobj:
        template = string.Template(fileobj.read())
    return template.safe_substitute(**context)



def timeit(func):
    """Decorator that logs the cost time of a function.
    """
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        start  = timer()
        result = func(*args, **kwargs)
        cost   = timer() - start
        logger.debug('<method: %s> finished in %2.2f sec' % (func.__name__, cost))
        return result
    return wrapped_func


def traceback(frame, parent=True):
    """Pick frame info from current caller's `frame`.

    Args:
        frame: :type:`frame` instance, use :func:`inspect.currentframe`.
        parent: whether to get outer frame (caller) traceback info, :data:`False` by default.

    Returns:
        :class:`inspect.Trackback` instance from :data:`frame` or its parent frame.
    """
    # Traceback(filename='<stdin>', lineno=1, function='<module>', code_context=None, index=None)
    if parent is True:
        # frame itself will always be placed @ the first index of its outerframes.
        outers = inspect.getouterframes(frame)
        traceback = (len(outers) == 1) and None or inspect.getframeinfo(outers[1][0])
    else:
        traceback = inspect.getframeinfo(frame)
    return traceback


def here(*segments):
    """Get abspath of current file (instead of __file__).

    This is to avoid "'__file__' is not defined" issue
    when parsing config file using `tornado.options.parse_config_file`.

    Args:
        *segments: path segments to be joint.

    Returns: absolute path joint with given segments against current file.
    """
    currentfile = traceback(inspect.currentframe()).filename
    currentpath = os.path.abspath(os.path.dirname(currentfile))
    return os.path.join(currentpath, *segments)
