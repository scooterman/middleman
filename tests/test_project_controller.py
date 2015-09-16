# -*- coding: utf-8 -*-
# author: victor

# noinspection PyUnresolvedReferences
import pytest

# noinspection PyUnresolvedReferences
from fixtures import user_f, user2_f

from middleman.controllers import project_controller
from middleman.core import error_codes
from middleman.exceptions import ApiException


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
