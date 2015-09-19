# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho
import pytest

# noinspection PyUnresolvedReferences
from fixtures import user_f

from middleman.controllers import user_controller
from middleman.exceptions import ApiException
from middleman.core import error_codes


def test_create(app):
    user = user_controller.create(app.config['SECRET_KEY'], email='cocada@cocada.com',
                                  name='John',
                                  password='cocada_123')

    assert user is not None
    assert user.password != 'cocada_123'

    return user


def test_create_big_email(app):
    user = user_controller.create(app.config['SECRET_KEY'],
                                  name='John',
                                  email='thisisahugeemailtosendljajajajakjlaja@ahahjahjaajjhaljçaçljaljçkajç'
                                        'lkjlçkalkjçjaçlkaaheuuehahuaeaeuea.com',
                                  password='cocada_123')

    assert user is not None
    assert user.password != 'cocada_123'

    return user


def test_create_big_password(app):
    with pytest.raises(ApiException) as e:
        user_controller.create(app.config['SECRET_KEY'],
                               name='John',
                               email='cocada@cocada.com',
                               password='alçkjsçajlsjafçjskjfdçjasdjfisjbidgjhieushosvos'
                                        'oudhfush!@#!52jlsg')

    assert e.value.code == 400
    assert e.value.reason == error_codes.VALIDATION_ERROR
    assert error_codes.PASSWORD_BIG in e.value.extra['password']


def test_invalid_email(app):
    with pytest.raises(ApiException) as e:
        user_controller.create(app.config['SECRET_KEY'], 'cocada', 'cocada_123')

    assert e.value.reason == error_codes.VALIDATION_ERROR
    assert e.value.extra
    assert error_codes.EMAIL_INVALID in e.value.extra['email']
    assert e.value.code == 400


def test_duplicate_user(app):
    user_controller.create(app.config['SECRET_KEY'], name='John', email='cocada@cocada.com', password='cocada_123')
    with pytest.raises(ApiException) as e:
        user_controller.create(app.config['SECRET_KEY'], name='John', email='cocada@cocada.com', password='cocada_123')

    assert e.value.reason == error_codes.EMAIL_ALREADY_REGISTERED
    assert e.value.code == 409


def test_verify_login_valid(user_f):
    assert user_controller.verify_login(user_f.email, 'cocada_123')


def test_verify_login_invalid(user_f):
    with pytest.raises(ApiException) as e:
        user_controller.verify_login(user_f.email, 'lololo')

    assert e.value.code == 404
    assert e.value.reason == error_codes.LOGIN_INVALID
