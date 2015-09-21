# -*- coding: utf-8 -*-
# Copyright (c) 2015, zup.com http://zup.com/, all rights reserved.
# author: victor
from middleman.database import db


def to_persist(entity):
    db.session.add(entity)


def save_all():
    db.session.commit()

def to_remove(entity):
    db.session.delete(entity)