__author__ = 'victor'

from middleman import db

class ModelAttributeType(object):
    STRING = 1
    TEXT = 2
    DECIMAL = 3
    INT = 4
    BOOLEAN = 5


class Model(db.Model):
    """
        A model is a representation of a speficied relationao object
        on a system.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)

    @staticmethod
    def create(name):
        return Model(name=name)

    def __repr__(self):
        return '<Model {0!r} {1!r}>'.format(self.id, self.name)

    def __str__(self):
        return self.name


class ModelAttribute(db.Model):
    """
        A model attribute is a column
        on a model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    attrtype = db.Column(db.Integer(), nullable=False)
    model_id = db.Column(db.Integer(), db.ForeignKey('model.id'), nullable=False)

    model = db.relationship('Model', uselist=False, backref='attributes')

    @staticmethod
    def create(name, attrtype, model):
        return ModelAttribute(name=name, attrtype=attrtype, model=model)

    def __repr__(self):
        return '<ModelAttribute {0!r} {1!r}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
