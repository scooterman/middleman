# -*- coding: utf-8 -*-
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy


class Table(sqlalchemy.Table):

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


def _make_table(db):
    def _make_table(*args, **kwargs):
        if len(args) > 1 and isinstance(args[1], db.Column):
            args = (args[0], db.metadata) + args[1:]
        info = kwargs.pop('info', None) or {}
        info.setdefault('bind_key', None)
        kwargs['info'] = info
        return Table(*args, **kwargs)
    return _make_table

db = SQLAlchemy()
db.Table = _make_table(db)
