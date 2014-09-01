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
from uuid import uuid4
from urlparse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
General SQLAlchemy helpers for easy scaling.

`ObjectId` uuid4-based object id for sharding (32-bit).

`create_session_factory` SQLAlchemy Session Class maker.

`get_host_from_uri` fetch host (port) from database URI as sharding key.
"""


__all__ = ('ObjectId', 'create_session_factory', 'get_host_from_uri',)


ObjectId = lambda: uuid4().hex


def create_session_factory(dburi, **options):
    """Create a single thread-based session (without scrope).

    DO NOT use scoped_session here due to single-thread model of Tornado.

    Args:
        dburi: database URI for connection.
        options: options to connect.

    Returns:
        SQLAlchemy session for accessing database.
    """
    engine  = create_engine(dburi, **options)
    return sessionmaker(bind=engine)


def get_host_from_uri(dburi):
    """Get host (& port) from the given database URI.

    Parse & pick the unique host+port string to identify
    the database server mainly for sharding/scaling.
    SQLite database connection string will be returned as
    the original URI.

    Examples:
        ParseResult(scheme='postgresql', netloc='scott:tiger@localhost:5432', path='/mydatabase', params='', query='', fragment='')
        ParseResult(scheme='sqlite', netloc='', path='//absolute/path/to/foo.db', params='', query='', fragment='')
    """
    result = urlparse(dburi)
    # for file-based SQLite & extrame case that we can't find netloc.
    if result.scheme == 'sqlite' or not result.netloc:
        return dburi

    # regular username/password based access.
    if '@' in result.netloc:
        return result.netloc.split('@')[-1]

    return result.netloc

