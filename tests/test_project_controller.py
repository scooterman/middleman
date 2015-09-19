# -*- coding: utf-8 -*-
# author: victor

# noinspection PyUnresolvedReferences
import pytest

# noinspection PyUnresolvedReferences
from fixtures import user_f, user2_f, project_f, project_model_f, project_model_attrs_f
from middleman import db

from middleman.controllers import project_controller
from middleman.core import error_codes
from middleman.exceptions import ApiException
from middleman.models.model import ModelAttributeType


def test_basic_project(user_f):
    project = project_controller.create('BasicApplication', user_f)

    assert project
    assert project.owner == user_f
    assert project.create_date


def test_duplicate_project(user_f):
    project_controller.create('BasicApplication', user_f)

    with pytest.raises(ApiException) as e:
        project_controller.create('BasicApplication', user_f)

    assert e.value.code == 403
    assert e.value.reason == error_codes.PROJECT_EXISTS


def test_duplicate_project_name_different_owners(user_f, user2_f):
    project1 = project_controller.create('BasicApplication', user_f)
    project2 = project_controller.create('BasicApplication', user2_f)

    assert project1 and project2


def test_project_by_hash(app, user_f):
    project1 = project_controller.create('BasicApplication', user_f)

    # we commit so we get an id for the project
    db.session.commit()

    pid, project = project_controller.project_by_hash(app.extensions['hasher'].encode(project1.id))

    assert pid
    assert project
    assert project == project1


def test_model_creation(app, project_f):
    # we commit so we get an id for the project
    db.session.commit()
    model = project_controller.create_model(app.extensions['hasher'].encode(project_f.id), 'Products', [])

    assert model
    assert model.project == project_f

    return model


def test_model_attributes(app, project_f):
    model = test_model_creation(app, project_f)
    attribute = project_controller.bind_attribute(model, 'name', 'STRING')

    assert attribute.model == model
    assert attribute.attrtype == ModelAttributeType.STRING


def test_deploy(project_model_attrs_f):
    db.session.commit()
    project_controller.deploy(project_model_attrs_f.owner, project_model_attrs_f, project_model_attrs_f.access_token)
