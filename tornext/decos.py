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

import logging
from tornext import utils

"""
Consolidated decorators.
"""

__all__ = ('cache',)


logger = logging.getLogger('tornext.%s' % __name__)


def decorate(wrapper):
    """Decorator helper with argument supports.

    Example:
        @decorate
        def my_decorator(func, *deco_args, **deco_kwargs):
            def wrapper(*func_args, **func_kwargs):
                print "from decorator:", deco_args, deco_kwargs
                func(*func_args, **func_kwargs)
            return wrapper
    """
    return lambda *args, **kwargs: lambda func: wrapper(func, *args, **kwargs)


@decorate
def cache(func, timeout=3600):
    def wrapper(self, *args, **kwargs):
        #cache_key = utils.get_cache_key(self.request)
        #logger.info('** Decorating: %s Timeout: %d' % (cache_key, timeout))
        # cachding the calculated response here

        return func(self, *args, **kwargs)
    return wrapper
