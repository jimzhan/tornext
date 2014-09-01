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

import uuid
import hmac
import hashlib

from tornado import web
from tornado import locale


__all__ = ('get_browser_locale', 'get_cache_key')


class RequestHandler(web.RequestHandler):

    def get_browser_locale(self, default="en_US"):
        """Determines the user's locale from ``Accept-Language`` header.

        Taken from `tornado.web.RequestHandler`#`get_browser_locale`.
        See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4

        Args:
            request: `tornado.httputils.HTTPServerRequest` instance.
            default: default locale code (en_US).

        Returns: Language code.
        """
        if "Accept-Language" in self.request.headers:
            languages = self.request.headers["Accept-Language"].split(",")
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


    def get_cache_key(self, namespace=None, secret=uuid.NAMESPACE_URL.hex):
        """Generate distributed cache key from the incoming request.

        Key components by order:
            full request url
            user's locale (default: en-us)
            prefix: default is None, prepare for user identity based caching.
        """
        message = [self.request.full_url(), self.get_browser_locale()]
        if namespace: message.insert(0, namespace)
        return hmac.new(secret, '|'.join(message), hashlib.sha1).hexdigest()
