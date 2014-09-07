#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornext.commands import Manager


if __name__ == '__main__':
    Manager(__doc__, options_first=True).dispatch()
