# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho

from middleman import db


def remove(model):
    db.delete(model)


def drop(table_name):
    db.drop_all(bind=table_name)
