# -*- coding: utf-8 -*-
# author: victor
from middleman import db
from middleman.models.project import Project


def project_by_name_owner(name, owner):
    return db.session.query(Project).filter(Project.name == name, Project.owner == owner).first()


def project_by_id(project_id):
    return db.session.query(Project).filter(Project.id == project_id).first()


def get_projects_for_user(owner):
    return db.session.query(Project).filter(Project.owner == owner).all()


def by_access_token(access_token):
    return db.session.query(Project).filter(Project.access_token == access_token).first()
