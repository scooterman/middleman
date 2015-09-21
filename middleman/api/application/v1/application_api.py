# -*- coding: utf-8 -*-
# Copyright zup. All rights reserved.
# 20/09/2015
# @author: Victor Vicene de Carvalho

from flask import Blueprint, request, jsonify
from middleman import ApiException
from middleman.acessors import to_persist, save_all

from middleman.controllers import project_controller
from middleman.acessors import model_acessor
from .serialization.generic_serialization import build_serializer

mod = Blueprint('applications', __name__)


def fetch_model(access_token, endpoint):
    project = project_controller.get_project_by_access_token(access_token)
    model = project_controller.model_by_name(project, endpoint)
    model_db_cached = project_controller.get_cached_model(model)

    return model_db_cached


@mod.route('/<endpoint>', methods=['GET'])
def custom_models_get(endpoint):
    model_db_cached = fetch_model(request.headers['X-Internal-AccessToken'], endpoint)

    serializer_class = build_serializer(model_db_cached)
    serializer = serializer_class(many=True)
    models = model_acessor.all_models(model_db_cached)

    return jsonify({'result': serializer.dump(models).data})


@mod.route('/<endpoint>', methods=['POST'])
def custom_model_post(endpoint):
    model_db_cached = fetch_model(request.headers['X-Internal-AccessToken'], endpoint)

    instance = model_db_cached(**request.json)
    to_persist(instance)

    serializer_class = build_serializer(model_db_cached)
    serializer = serializer_class()
    save_all()

    return jsonify({'result': serializer.dump(instance).data})


@mod.route('/<endpoint>/<model_id>', methods=['GET'])
def custom_model_get(endpoint, model_id):
    model_db_cached = fetch_model(request.headers['X-Internal-AccessToken'], endpoint)

    instance = model_acessor.find(model_db_cached, model_id)

    if not instance:
        raise ApiException(code=404)

    serializer_class = build_serializer(model_db_cached)
    serializer = serializer_class()

    return jsonify(serializer.dump(instance).data)


@mod.route('/<endpoint>/<model_id>', methods=['PUT'])
def custom_model_put(endpoint, model_id):
    model_db_cached = fetch_model(request.headers['X-Internal-AccessToken'], endpoint)

    instance = model_acessor.find(model_db_cached, model_id)

    if not instance:
        raise ApiException(code=404)

    for key, value in request.json.items():
        setattr(instance, key, value)

    to_persist(instance)
    save_all()

    serializer_class = build_serializer(model_db_cached)
    serializer = serializer_class()

    return jsonify({'result': serializer.dump(instance).data})


@mod.route('/<endpoint>/<model_id>', methods=['DELETE'])
def custom_model_delete(endpoint, model_id):
    model_db_cached = fetch_model(request.headers['X-Internal-AccessToken'], endpoint)

    instance = model_acessor.find(model_db_cached, model_id)

    if not instance:
        raise ApiException(code=404)

    model_acessor.remove(instance)
    save_all()

    return 'OK', 200
