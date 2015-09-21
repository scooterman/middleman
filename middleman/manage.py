#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Work out the project module name and root directory, assuming that this file
# is located at [project]/manage.py
PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(os.path.dirname(os.path.realpath(__file__)))

# Check that the project module can be imported.
try:
    __import__(PROJECT_MODULE_NAME)
except ImportError:
    # Couldn't import the project, place it on the Python path and try again.
    sys.path.append(PROJECT_DIR)
    try:
        __import__(PROJECT_MODULE_NAME)
    except ImportError:
        sys.stderr.write("Error: Can't import the \"%s\" project module.\n" %
                         PROJECT_MODULE_NAME)
        sys.exit(1)

from flask.ext.script import Manager, Server, prompt_bool
from flask import current_app

from middleman import create_app
from middleman.database import db

from middleman.controllers import user_controller

manager = Manager(create_app())
manager.add_option('-e', '--env', dest='env_name', required=False, default='DEVELOPMENT')
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


class ServerTest(Server):
    """Run server in testing env
    """

    def handle(self, app, host, port, use_debugger, use_reloader,
               threaded, processes, passthrough_errors):
        with app.test_request_context():
            dropdb(confirm=False)
            syncdb(default_data=True, sample_data=True)
            super(ServerTest, self).handle(app, host, port, use_debugger,
                                           use_reloader, threaded, processes, passthrough_errors)

    def run(self):
        raise NotImplementedError


manager_test = Manager(help=ServerTest.__doc__)
manager_test.add_command('runserver', ServerTest(host='0.0.0.0', port=5000))
manager.add_command('test', manager_test)


@manager.command
def dropdb(confirm=True):
    """Drops database tables
    """
    if not confirm or prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def syncdb():
    """Creates database tables from sqlalchemy models
    """
    db.create_all()


@manager.command
def resetdb():
    """Recreates database tables (same as issuing 'dropdb' and then 'syncdb')
    """
    dropdb()
    syncdb()


@manager.command
def createrole(name, description=None):
    """
    Creates a new role
    :return:
    """

    from middleman.models import Role

    role = Role.create(name, description)
    db.session.add(role)
    db.session.commit()


@manager.command
def createuser(name, email, password, role):
    """
    Creates a new user with specified roles
    :return:
    """

    from middleman.models import Role

    user = user_controller.create(current_app.config['SECRET_KEY'], name, email, password)

    role = db.session.query(Role).filter(Role.name == role).one()
    user_controller.set_roles(user, role)
    db.session.add(user)
    db.session.commit()


@manager.command
def removeuser(email):
    from middleman.models import User

    user = db.session.query(User).filter(User.email == email).one()
    db.session.delete(user)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
