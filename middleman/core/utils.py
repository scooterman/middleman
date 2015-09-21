# -*- coding: utf-8 -*-
# author: victor
from functools import wraps
from flask import request
from middleman.acessors import save_all

from middleman.exceptions import ApiException
from . import error_codes


def validate(locals_dict, validate_map):
    """
    Itera por todos os campos do dicionario e aplica a lista de validadores:
    obs: validadores no formato (<funcao>, 'reason')

    :param validate_map: o dicionario de validação
    """
    result = {}
    for key in filter(lambda k: k in validate_map and k in locals_dict, locals_dict):
        if not locals_dict[key]:
            continue

        validators = validate_map[key]
        items = [validator_item[1] for validator_item in validators if not validator_item[0](locals_dict[key])]

        if items:
            result[key] = items

    if result:
        raise ApiException(error_codes.VALIDATION_ERROR, result, code=400)


def strip(locals_dict, *fields):
    """
    Executa um trim nos campos especificados
    :param fields: a lista de campos a ser executado o trim
    """
    for item in fields:
        if item in locals_dict:
            locals_dict[item] = locals_dict[item].strip()


def application_config():
    ctx_path = request.path
    ctx_path = ctx_path if not ctx_path.endswith('/') else ctx_path[:-1]
    app_config = {
        'contextPath': ctx_path,
    }
    return app_config


def persist(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        result = f(*args, **kwargs)
        save_all()
        return result

    return wrap
