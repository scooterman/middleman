# -*- coding: utf-8 -*-
# Copyright (c) 2015, 99truck.com Inc. http://99truck.com/, all rights reserved.
import os
import sys

from flask import Flask, Response
from flask.ext.environments import Environments
from flask_marshmallow import Marshmallow

from flask.ext.security import Security, SQLAlchemyUserDatastore
from hashids import Hashids

from .database import db
from middleman.exceptions import ApiException
from middleman.settings import from_env_name
from middleman.core.utils import application_config
from middleman.models.users import Role
from middleman.models.users import User

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(__file__))
)

# Defines the directory of the python interpreter
ACTIVATE_THIS = os.path.join(PROJECT_DIR, os.pardir, 'bin', 'activate_this.py')
PYTHON_BIN = os.path.dirname(sys.executable)
if os.path.exists(ACTIVATE_THIS):
    PYTHON_BIN = os.path.join(PROJECT_DIR, os.pardir, 'bin')

if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # Assume that the presence of 'activate_this.py' in the python bin/
    # directory means that we're running in a virtual environment. Set the
    # variable root to $VIRTUALENV/var.
    PROJECT_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
    if not os.path.exists(PROJECT_ROOT):
        os.mkdir(PROJECT_ROOT)
else:
    # Set the variable root to the local configuration location (which is
    # ignored by the repository).
    PROJECT_ROOT = os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME)

# Adds the project in the python path
syspath = os.path.join(PROJECT_DIR, os.pardir)
if syspath not in sys.path:
    sys.path.insert(0, syspath)

ma = Marshmallow()


def create_app(env_name='DEVELOPMENT'):
    # Flask application
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.update(PROJECT_ROOT=PROJECT_ROOT)
    app.config.update(PROJECT_DIR=PROJECT_DIR)

    # Flask environment
    env = Environments(app, default_env=from_env_name(env_name))
    env.from_object('{0}.settings'.format(__name__))
    app.extensions['env'] = env

    # Create database connection object
    db.app = app  # RuntimeError: application not registered on db
    # instance and no application bound to current context
    db.init_app(app)
    ma.init_app(app)

    app.extensions['ma'] = ma
    app.extensions['db'] = db

    hasher = Hashids(salt=str(app.config['SECRET_KEY']), min_length=10)
    app.extensions['hasher'] = hasher

    # Flask security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    app.extensions['user_datastore'] = user_datastore
    app.extensions['security'] = security

    from .api.application import v1 as application_v1

    application_v1.setup(app)

    # Templates
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
        return value.strftime(format)

    # Context
    @app.context_processor
    def inject_application_config():
        return {
            'app_config': application_config()
        }

    @app.errorhandler(TypeError)
    def handle_type_error(error):
        response = Response(status=400)
        return response

    @app.errorhandler(ApiException)
    def handle_type_error(error):
        return error.to_response()

    return app
