# -*- coding: utf-8 -*-
# Copyright zup. All rights reserved.
# 20/09/2015
# @author: Victor Vicene de Carvalho
from middleman import ma

def build_serializer(model_class):
    class CustomSerializer(ma.ModelSchema):
        class Meta:
            model = model_class

    return CustomSerializer
