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

"""
common logging tools set with colorful console logs supports
"""
import sys
import logging
import logging.config

from clint.textui import colored


__all__ = ('getLogger',)


_configured = False


CONFIG = {
    'root': { 'level': 'DEBUG', 'handlers': ('console',) },

    'version': 1,

    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
        #    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': { 'format': '%(levelname)s %(message)s' },
    },

    'handlers': {
         'console': {
            'class':     '{pkg}.ConsoleHandler'.format(pkg=__name__),
            'level':     'DEBUG',
            'formatter': 'verbose',
            'stream':    'ext://sys.stdout',
        }
    }
}


def getLogger(package):

    global _configured

    if not _configured:
        logging.config.dictConfig(CONFIG)
        _configured = True

    return logging.getLogger(package)



class ConsoleHandler(logging.StreamHandler):
    """Console based handler with colors supports.

    * Based on `clint`, add colors supports for each logging level.
    * Segregate the logging stream to sys.stdout and sys.stderr, while
        only error stream goes out int sys.stderr by default.

    Attributes:
        * COLORS: colored lambda shortcuts with logging's levels as keys.
    """

    COLORS = {
        logging.DEBUG:      colored.blue,
        logging.INFO:       colored.green,
        logging.WARN:       colored.yellow,
        logging.ERROR:      colored.magenta,
        logging.CRITICAL:   colored.red
    }

    def __init__(self, *args, **kwargs):
        super(ConsoleHandler, self).__init__(*args, **kwargs)
        self.stream = None  # reset the default stream.


    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()


    def _emit(self, record, stream):
        self.stream = stream
        logging.StreamHandler.emit(self, record)


    def emit(self, record):
        stream = (record.levelno >= logging.ERROR) and sys.stderr or sys.stdout
        self._emit(record, stream)


    def format(self, record):
        message = self.formatter.format(record)
        return self.is_tty and self.COLORS[record.levelno](message) or message


    def flush(self):
        # @see(http://bugs.python.org/issue6333)
        if self.stream and hasattr(self.stream, 'flush') and not self.stream.closed:
            logging.StreamHandler.flush(self)
