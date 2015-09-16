# -*- coding: utf-8 -*-
# author: victor
import datetime
import random

from middleman import db


class Project(db.Model):
    """
        A project contains a set of models and an access_token.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    access_token = db.Column(db.String(16), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', uselist=False, backref='projects')

    @staticmethod
    def create(name, owner):
        access_token = '%016x' % random.randrange(16 ** 16)
        return Project(name=name, access_token=access_token, owner=owner,
                       create_date=datetime.datetime.now())

    def __repr__(self):
        return '<Project {0!r} {1!r}>'.format(self.id, self.name)
