# -*- coding: utf-8 -*-
# Copyright zup. All rights reserved.
# 20/09/2015
# @author: Victor Vicene de Carvalho
from flask import Blueprint, request, current_app, jsonify
from flask.ext.security import login_required, current_user

from middleman.core.utils import persist
from middleman.controllers import project_controller

from .serialization import *

mod = Blueprint('projects', __name__)


@mod.route('/', methods=['POST'])
@login_required
@persist
def create_project():
    return jsonify(project_serializer.dump(project_controller.create(request.json['name'], current_user)).data)


@mod.route('/', methods=['GET'])
@login_required
def get_projects():
    return jsonify({'projects': projects_serializer.dump(project_controller.get_user_projects(current_user)).data})


@mod.route('/<hash_id>', methods=['GET'])
@login_required
def get_project(hash_id):
    return jsonify(full_project_serializer.dump(
        project_controller.get_project(current_user,
                                       current_app.extensions['hasher'].decode(hash_id)[0])).data)


@mod.route('/<hash_id>/models', methods=['POST'])
@login_required
@persist
def set_project_models(hash_id):
    project = project_controller.get_project(current_user,
                                             current_app.extensions['hasher'].decode(hash_id)[0])

    for model in request.json['models']:
        project_controller.create_model(project, model['name'], model['attributes'] if 'attributes' in model else [])

    return 'ok', 200


@mod.route('/<project_hash>/models/<model_hash>', methods=['PUT', 'DELETE'])
@login_required
@persist
def update_model(project_hash, model_hash):
    project = project_controller.get_project(current_user,
                                             current_app.extensions['hasher'].decode(project_hash)[0])

    model_id = current_app.extensions['hasher'].decode(model_hash)[0]

    model = project_controller.get_model(project, model_id)

    if request.method == 'PUT':
        project_controller.update_model(model, request.json['attributes'])
    elif request.method == 'DELETE':
        project_controller.remove_model(model)

    return 'ok', 200


@mod.route('/<project_hash>/deploy', methods=['POST'])
@login_required
def deploy(project_hash):
    project = project_controller.get_project(current_user,
                                             current_app.extensions['hasher'].decode(project_hash)[0])

    project_controller.deploy(project)
    return 'ok', 200


@mod.route('/<project_hash>/undeploy', methods=['POST'])
@login_required
def undeploy(project_hash):
    project = project_controller.get_project(current_user,
                                             current_app.extensions['hasher'].decode(project_hash)[0])

    project_controller.undeploy(project)
    return 'ok', 200
