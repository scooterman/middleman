# -*- coding: utf-8 -*-
# Copyright zup. All rights reserved.
# 20/09/2015
# @author: Victor Vicene de Carvalho

def setup(app):
    """
    Registers all blueprints for application version 1
    """
    from . import project_api
    from . import user_api
    from . import application_api

    app.register_blueprint(project_api.mod, url_prefix='/api/v1/projects')
    app.register_blueprint(user_api.mod, url_prefix='/api/v1')
    app.register_blueprint(application_api.mod, url_prefix='/api/v1/apps')
