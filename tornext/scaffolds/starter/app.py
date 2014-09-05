#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.options import options

from tornext.core import Application
from tornext.cache.redis import RedisCache

import urls


def main():
    app = Application(urls.patterns, 'settings.py')
    app.cache = RedisCache(['redis://localhost:6379'])
    app.start(options.port)


if __name__ == "__main__":
    main()
