from flask.ext.login import UserMixin, make_secure_token
from flask.ext.security import RoleMixin

from middleman import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    name = db.Column(db.String(), nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def create(name, email, password):
        return User(name=name, email=email, password=password)

    def __repr__(self):
        return '<User {0!r} {1!r}>'.format(self.id, self.password)

    def get_auth_token(self):
        return make_secure_token(self.email, str(self.id), self.password)
