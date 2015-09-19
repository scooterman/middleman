# -*- coding: utf-8 -*-
# author: victor
from flask import current_app, Blueprint, jsonify, request

from middleman import db
from middleman.acessors import project_acessor, to_persist, save_all
from middleman.exceptions import ApiException
from middleman.core import error_codes
from middleman.models.model import ModelAttributeType, ModelAttribute, Model
from middleman.models.project import Project
from middleman.acessors import model_acessor


def create(name, owner):
    project = project_acessor.project_by_name_owner(name, owner)

    if project:
        raise ApiException(error_codes.PROJECT_EXISTS, code=403)

    project = Project.create(name, owner)
    to_persist(project)

    return project


def project_by_hash(project_hash):
    project_id = current_app.extensions['hasher'].decode(project_hash)[0]
    project = project_acessor.project_by_id(project_id)

    if not project:
        raise ApiException(code=404)

    return project_id, project


def undeploy(project):
    if project.deployed:
        for model in project.models:
            unregister_model(model)

        project.deployed = False

    to_persist(project)
    save_all()


def deploy(user, project, access_token):
    if user != project.owner:
        raise ApiException(code=403)

    if access_token != project.access_token:
        raise ApiException(code=403)

    undeploy(project)

    for model in project.models:
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

        db.create_all()

        mod = Blueprint(model.name.lower(), model.table_name())

        @mod.route(model.name, methods=['GET'])
        def custom_model_get():
            models = db.session.get(CustomModel).all()

            return jsonify({'result': models})

        @mod.route(model.name, methods=['POST'])
        def custom_model_post():
            _model = CustomModel(**request.json)
            db.session.add(_model)
            db.session.commit()

        @mod.route(model.name + '/<model_id>', methods=['PUT'])
        def custom_model_put(model_id):
            _model = db.session.query(CustomModel).get(model_id)

            for key, value in request.json:
                setattr(_model, key, value)

            db.session.add(_model)
            db.session.commit()

        @mod.route(model.name + '/<model_id>', methods=['DELETE'])
        def custom_model_delete(model_id):
            _model = db.session.query(CustomModel).get(model_id)
            db.session.delete(_model)
            db.session.commit()

        current_app.register_blueprint(mod, url_prefix='/api/' +
                                                       current_app.extensions['hasher'].encode(project.id) + '/')


def unregister_model(model):
    model_acessor.remove(model.id)
    model_acessor.drop(model.table_name())


def create_model(project_hash, model_name, attribute_def_list):
    from middleman.controllers import project_controller

    project_id, project = project_controller.project_by_hash(project_hash)

    if any((model.name == model_name for model in project.models)):
        raise ApiException(error_codes.MODEL_ALEADY_DEFINED, code=400)

    model = Model.create(model_name, project)
    to_persist(model)

    for attribute_def in attribute_def_list:
        bind_attribute(model, **attribute_def)

    return model


def model_by_hash(model_hash):
    pass


def bind_attribute(model, name, attrtype):
    if any((attr.name == name for attr in model.attributes)):
        raise ApiException(error_codes.ATTRIBUTE_ALEADY_DEFINED, code=400)

    if attrtype not in ModelAttributeType.__members__.keys():
        raise ApiException(error_codes.ATTRIBUTE_TYPE_UNKNOWN, code=400)

    attribute = ModelAttribute.create(name, ModelAttributeType[attrtype], model)
    to_persist(attribute)

    return attribute
