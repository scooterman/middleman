# -*- coding: utf-8 -*-
import os
from datetime import timedelta

def from_env_name(env_name):
    env_name = env_name.upper()
    if env_name in ('DEV', 'DEVELOPMENT'):
        env_name = 'DEVELOPMENT'
    elif env_name in ('TEST', 'TESTING'):
        env_name = 'TESTING'
    elif env_name in ('STAG', 'STAGING'):
        env_name = 'STAGING'
    elif env_name in ('PROD', 'PRODUCTION'):
        env_name = 'PRODUCTION'
    else:
        ValueError('env_name invalid')
    return env_name


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\tP\xd6\xa1z\x81f\xc3\x9b!\xa0\xccp\xe2i\x1b\x1a\x1c40\x9a\x9f\xca\x95\x18\x85\x8b"\xc2\x11\xea\xd9'
    PIDFILE_PATH = os.path.join('/', 'var', 'run', 'middleman_%s.pid')

    # Flask-Babel
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/../../vendor/databases/sqlite3/middleman.db' \
        .format(os.path.dirname(os.path.realpath(__file__)))
    SQLALCHEMY_ECHO = False

    # Flask-Security
    SECURITY_URL_PREFIX = '/security'
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_EMAIL_SENDER = 'no-reply@localhost'
    SECURITY_SEND_REGISTER_EMAIL = True

    # Flask-WTF
    WTF_CSRF_CHECK_DEFAULT = False

class Testing(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True
    CELERY_ALWAYS_EAGER = True

class Development(Config):
    DEBUG = True
    PIDFILE_PATH = os.path.join('/', 'var', 'run', 'daemons', 'middleman_%s.pid')
    SQLALCHEMY_ECHO = True

class Staging(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

class Production(Config):
    pass
