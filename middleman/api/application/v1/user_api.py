# -*- coding: utf-8 -*-
# @author: Victor Vicene de Carvalho

from flask import Blueprint, request, current_app
from flask.ext.security import login_user, login_required, logout_user

from middleman.core.utils import persist
from middleman.controllers import user_controller

mod = Blueprint('users', __name__)

@mod.route('/register', methods=['POST'])
@persist
def register():
    user_controller.create(current_app.config['SECRET_KEY'], request.json['name'], request.json['email'],
                           request.json['password'])

    return 'ok', 200


@mod.route('/login', methods=['POST'])
def login():
    user = user_controller.verify_login(request.json['email'], request.json['password'])
    login_user(user, True)

    return 'ok', 200


@mod.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return 'ok', 200
