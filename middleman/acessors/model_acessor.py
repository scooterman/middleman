# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho

from middleman import db
from middleman.models import ModelAttributeType


def remove(model):
    db.session.delete(model)


def drop(table_name):
    db.drop_all(bind=table_name)


def build_model(model):
    class CustomModel(db.Model):
        __tablename__ = model.table_name()
        id = db.Column(db.Integer(), primary_key=True)

    for attribute in model.attributes:
        if attribute.attrtype == ModelAttributeType.STRING:
            setattr(CustomModel, attribute.name, db.Column(db.String()))
        elif attribute.attrtype == ModelAttributeType.INT:
            setattr(CustomModel, attribute.name, db.Column(db.Integer()))
        elif attribute.attrtype == ModelAttributeType.BOOLEAN:
            setattr(CustomModel, attribute.name, db.Column(db.Boolean()))
        elif attribute.attrtype == ModelAttributeType.DECIMAL:
            setattr(CustomModel, attribute.name, db.Column(db.Numeric()))
        elif attribute.attrtype == ModelAttributeType.TEXT:
            setattr(CustomModel, attribute.name, db.Column(db.Text()))

    return CustomModel


def all_models(model_class):
    return db.session.query(model_class).all()


def find(model_class, model_id):
    return db.session.query(model_class).filter(model_class.id == model_id).first()
