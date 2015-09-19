# -*- coding: utf-8 -*-
# author: victor

import pytest

from middleman.models import Project, Model, ModelAttribute, ModelAttributeType


@pytest.fixture
def project_f(session, user_f):
    project = Project.create('MyProject', user_f)
    session.add(project)

    return project


@pytest.fixture
def project_model_f(session, user_f):
    project = Project.create('MyProject', user_f)
    session.add(project)

    model = Model.create('Products', project)
    session.add(model)

    return project

@pytest.fixture
def project_model_attrs_f(session, user_f):
    project = Project.create('MyProject', user_f)
    session.add(project)

    model = Model.create('Products', project)
    session.add(model)

    attr = ModelAttribute.create('name', ModelAttributeType.STRING, model)
    session.add(attr)

    return project