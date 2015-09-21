# -*- coding: utf-8 -*-
# author: victor
from flask import current_app

from middleman import db
from middleman.acessors import project_acessor, to_persist, save_all, to_remove
from middleman.exceptions import ApiException
from middleman.core import error_codes
from middleman.models.model import ModelAttributeType, ModelAttribute, Model
from middleman.models.project import Project
from middleman.acessors import model_acessor


def get_project_by_access_token(access_token):
    project = project_acessor.by_access_token(access_token)

    if not project:
        raise ApiException(code=404)

    return project


def model_by_name(project, model_name):
    model = next(filter(lambda m: m.name.lower() == model_name.lower(), project.models), None)

    if not model:
        raise ApiException(code=404)

    return model


def create(name, owner):
    project = project_acessor.project_by_name_owner(name, owner)

    if project:
        raise ApiException(error_codes.PROJECT_EXISTS, code=403)

    project = Project.create(name, owner)
    to_persist(project)

    return project


def get_user_projects(user):
    return project_acessor.get_projects_for_user(user)


def get_project(user, project_id):
    project = project_acessor.project_by_id(project_id)

    if not project:
        raise ApiException(code=404)

    if user != project.owner:
        raise ApiException(code=403)

    return project


def undeploy(project):
    if project.deployed:
        for model in project.models:
            unregister_model(model)

        project.deployed = False

    to_persist(project)
    save_all()


_model_cache = {}


def build_model_db(model):
    if model.id in _model_cache:
        return _model_cache[model.id]

    _model_cache[model.id] = model = \
        model_acessor.build_model(model)

    return model


def get_cached_model(model):
    return build_model_db(model)


def deploy(project):
    undeploy(project)

    for model in project.models:
        build_model_db(model)

    db.create_all()


def unregister_model(model):
    model_acessor.remove(model.id)
    model_acessor.drop(model.table_name())


def get_model(project, model_id):
    model = next(filter(lambda x: x.id == model_id, project.models), None)

    if not model:
        raise ApiException(code=404)

    return model


def create_model(project, model_name, attribute_def_list):
    if any((model.name == model_name for model in project.models)):
        raise ApiException(error_codes.MODEL_ALEADY_DEFINED, code=400)

    model = Model.create(model_name, project)
    to_persist(model)

    update_model(model, attribute_def_list)

    return model


def update_model(model, attributes):
    for attribute_def in attributes:
        bind_attribute(model, **attribute_def)


def remove_model(model):
    to_remove(model)


def bind_attribute(model, name, attrtype):
    if any((attr.name == name for attr in model.attributes)):
        raise ApiException(error_codes.ATTRIBUTE_ALEADY_DEFINED, code=400)

    if attrtype not in ModelAttributeType.__members__.keys():
        raise ApiException(error_codes.ATTRIBUTE_TYPE_UNKNOWN, code=400)

    attribute = ModelAttribute.create(name, ModelAttributeType[attrtype], model)
    to_persist(attribute)

    return attribute
