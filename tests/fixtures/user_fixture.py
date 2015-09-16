# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho

import datetime

import pytest
from flask_security.utils import encrypt_password

from middleman.models.users import User

@pytest.fixture
def user_f(app, session):
    _user = User.create('user@gmail.com', encrypt_password('cocada_123'))
    _user.confirmed_at = datetime.datetime(2015, 5, 5, 10, 0, 0)
    _user.active = True

    session.add(_user)

    return _user