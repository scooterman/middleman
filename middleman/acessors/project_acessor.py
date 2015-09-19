# -*- coding: utf-8 -*-
# author: victor
from middleman import db
from middleman.models.project import Project


def project_by_name_owner(name, owner):
    return db.session.query(Project).filter(Project.name == name, Project.owner == owner).first()


def project_by_id(project_id):
    return db.session.query(Project).filter(Project.id == project_id).first()