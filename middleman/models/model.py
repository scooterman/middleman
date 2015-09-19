import enum

__author__ = 'victor'

from middleman import db


class ModelAttributeType(enum.IntEnum):
    STRING = 1
    TEXT = 2
    DECIMAL = 3
    INT = 4
    BOOLEAN = 5


class Model(db.Model):
    """
        A model is a representation of a speficied relationao objecte:
        on a system.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', single_parent=True, uselist=False, backref='models',
                              cascade='all, delete, delete-orphan')

    @staticmethod
    def create(name, project):
        return Model(name=name, project=project)

    def __repr__(self):
        return '<Model {0!r} {1!r}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    def table_name(self):
        return self.name + '_' + self.project.name + '_' + self.project.owner.name


class ModelAttribute(db.Model):
    """
        A model attribute is a column
        on a model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    attrtype = db.Column(db.Integer(), nullable=False)
    model_id = db.Column(db.Integer(), db.ForeignKey('model.id'), nullable=False)

    model = db.relationship('Model', single_parent=True, uselist=False, backref='attributes',
                            cascade='all, delete, delete-orphan')

    @staticmethod
    def create(name, attrtype, model):
        return ModelAttribute(name=name, attrtype=attrtype, model=model)

    def __repr__(self):
        return '<ModelAttribute {0!r} {1!r}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
