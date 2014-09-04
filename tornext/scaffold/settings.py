#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornext.utils import here


# general settings #
debug = True
#ui_modules = apps.uimodules

# auth settings #
cookie_secret = '${cookie_secret}'

# templates settings
template_path = here('templates')

# static files settings #
static_path = here('assets')


# Cache Settings #
cache = {}
cache['urls'] = ('redis://127.0.0.1:6379',)

# Database Settings #
database = {}
database['urls'] = ('sqlite:///tmp/dev.sqlite',)
