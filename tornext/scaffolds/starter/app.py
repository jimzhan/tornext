#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado
from tornado.options import options

from tornext.web import Application
from tornext.cache.redis import RedisCache

import urls


def main():
    tornado.options.parse_command_line()
    app = Application(urls.patterns)
    app.cache = RedisCache(['redis://localhost:6379'])
    app.start(options.port)


if __name__ == "__main__":
    main()
