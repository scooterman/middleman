# -*- coding: utf-8 -*-
# Copyright zup. All rights reserved.
# 20/09/2015
# @author: Victor Vicene de Carvalho

from flask import current_app

from middleman.models import Project, Model, ModelAttribute, ModelAttributeType
from middleman import ma
from marshmallow import fields


class ProjectSchema(ma.ModelSchema):
    id = fields.Function(lambda obj: current_app.extensions['hasher'].encode(obj.id))

    class Meta:
        model = Project
        fields = ('name', 'access_token', 'id')

class AttributesSchema(ma.ModelSchema):
    id = fields.Function(lambda obj: current_app.extensions['hasher'].encode(obj.id))
    attrtype = fields.Function(lambda obj: ModelAttributeType(obj.attrtype).name)

    class Meta:
        model = ModelAttribute
        fielsd = ('name', 'attrtype')

class ModelSchema(ma.ModelSchema):
    id = fields.Function(lambda obj: current_app.extensions['hasher'].encode(obj.id))
    attributes = fields.Nested(AttributesSchema, many=True)

    class Meta:
        model = Model
        fields = ("name", "attributes")


class CompleteProjectSchema(ma.ModelSchema):
    models = fields.Nested(ModelSchema, many=True)

    class Meta:
        model = Project
        fields = ('name', 'access_token', 'models')


project_serializer = ProjectSchema()
projects_serializer = ProjectSchema(many=True)
full_project_serializer = CompleteProjectSchema()
model_serializer = ModelSchema()
