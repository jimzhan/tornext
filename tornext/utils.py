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

import os
import sys
import site
import string

from hashlib import md5
from urllib import urlencode
from tornado import locale


__all__ = ('add_libs', 'decorate', 'get_browser_locale', 'get_cache_key')


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


def get_browser_locale(request, default="en_US"):
    """Determines the user's locale from ``Accept-Language`` header.

    Taken from `tornado.web.RequestHandler`#`get_browser_locale`.
    See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4

    Args:
        request: `tornado.httputils.HTTPServerRequest` instance.
        default: default locale code (en_US).

    Returns: Language code.
    """
    if "Accept-Language" in request.headers:
        languages = request.headers["Accept-Language"].split(",")
        locales = []
        for language in languages:
            parts = language.strip().split(";")
            if len(parts) > 1 and parts[1].startswith("q="):
                try:
                    score = float(parts[1][2:])
                except (ValueError, TypeError):
                    score = 0.0
            else:
                score = 1.0
            locales.append((parts[0], score))
        if locales:
            locales.sort(key=lambda pair: pair[1], reverse=True)
            codes = [l[0] for l in locales]
            return locale.get(*codes).code
    return locale.get(default).code


def get_cache_key(request, prefix=None):
    """Generate distributed cache key from the incoming request.

    Key components by order:
        full request url
        user's locale (default: en-us)
        prefix: default is None, prepare for user identity based caching.
    """
    context = md5()
    if prefix: context.update(prefix)
    context.update(request.full_url())
    context.update(get_browser_locale(request))
    return context.hexdigest()


def get_hash_from_dict(dictionary, ignore_none=False):
    """Generate md5-based hash from the given dictionary.

    Args:
        dictionary (dict): dict to be hashed.
        ignore_none (bool): whether to ignore the items with None values.

    Returns:
        md5-based hash string.
    """
    if ignore_none:
        dictionary = dict([(k, v) for k, v in dictionary.items() if v is not None])
    return md5(urlencode(dictionary)).hexdigest()


def Template(template, **context):
    """
    Simple shortcut to `string.Template`, using safe_substitute method.

    Usage:
        Template('Hello ${name}', name='someone')  => 'Hello someone'

    Args:
        template (str): raw string template follows `string.Template` rules.
        context (dict): context of the string template.

    Returns:
        Substituted string by merging raw string template and its context.
    """
    return string.Template(template).safe_substitute(**context)
