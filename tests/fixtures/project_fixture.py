# -*- coding: utf-8 -*-
# author: victor

import pytest

from middleman.models.project import Project


@pytest.fixture
def project_f(session, user_f):
    project = Project.create('MyProject', user_f)
    session.add(project)

    return project
