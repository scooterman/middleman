# -*- coding: utf-8 -*-
# Copyright (c) 2015, Fittz, Inc. http://fittz.com.br/, all rights reserved.
# @author: Victor Vicene de Carvalho

from flask.ext.security.utils import encrypt_password, verify_password
from validate_email import validate_email

from middleman.models.users import User
from middleman.acessors import user_acessor, to_persist
from middleman.core.utils import validate, strip
from middleman.exceptions import ApiException
from middleman.core import error_codes as codes

validate_creation = {
    'email': [(validate_email, codes.EMAIL_INVALID)],
    'password': [(lambda password: len(password) > 4, codes.PASSWORD_SMALL),
                 (lambda password: len(password) < 50, codes.PASSWORD_BIG)]
}

USER_SALT = b'user_controller'


def create(secret_key, name, email, password):
    """
    Cria um novo usuário
    :param secret_key: O secret para encodar o token de confirmação
    :return: o usuário criado
    """

    strip(locals(), 'email', 'password')
    validate(locals(), validate_creation)

    if user_acessor.user_by_email(email):
        raise ApiException(codes.EMAIL_ALREADY_REGISTERED, email)

    user = User.create(name, email, encrypt_password(password))
    to_persist(user)

    return user


def set_roles(user, *roles):
    user.roles += roles


def get_user(email):
    return user_acessor.user_by_email(email)


def user_by_email(email):
    return user_acessor.user_by_email(email)


def verify_login(email, password):
    user = user_acessor.user_by_email(email)

    if not user:
        raise ApiException(codes.LOGIN_INVALID, code=404)

    if verify_password(password, user.password):
        return user

    raise ApiException(codes.LOGIN_INVALID, code=404)
