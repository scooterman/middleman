# -*- coding: utf-8 -*-
# author: victor
from middleman.acessors import project_acessor, to_persist
from middleman.exceptions import ApiException
from middleman.core import error_codes
from middleman.models.project import Project


def create(name, owner):
    project = project_acessor.project_by_name_owner(name, owner)

    if project:
        raise ApiException(error_codes.PROJECT_EXISTS, code=403)

    project = Project.create(name, owner)
    to_persist(project)

    return project
