# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho
import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from middleman import create_app


@pytest.fixture(scope='module')
def drop_database():
    _app = create_app(env_name='TEST')
    ctx = _app.app_context()
    ctx.push()

    from middleman import db

    db.drop_all()


@pytest.fixture
def app(drop_database, request):
    _app = create_app(env_name='TEST')

    ctx = _app.app_context()
    ctx.push()

    from middleman import db

    db.drop_all()
    db.create_all()

    request.addfinalizer(lambda: ctx.pop())

    return _app


@pytest.fixture(scope='function')
def session(app, request):
    """Creates a new database session for a test."""
    from middleman import db

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    _session = db.create_scoped_session(options=options)

    db.session = _session

    def finalize():
        transaction.rollback()
        connection.close()
        _session.remove()

    request.addfinalizer(finalize)
    return _session
