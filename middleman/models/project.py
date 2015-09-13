__author__ = 'victor'

from middleman import db

'''
Associates a batch of users to a batch of projects
'''
project_users = db.Table('project_users',
                         db.Column('project_id', db.Integer(), db.ForeignKey('project.id')),
                         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))


class Project(db.Model):
    """
        A project contains a set of models and an access_token.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    access_token = db.Column(db.String(1024), nullable=False)

    @staticmethod
    def create(name, access_token):
        return Project(name=name, access_token=access_token)

    def __repr__(self):
        return '<Project {0!r} {1!r}>'.format(self.id, self.name)
