# -*- coding: utf-8 -*-
from flask import jsonify


class ApiException(Exception):
    def __init__(self, reason=None, extra=None, code=409):
        self.reason = reason
        self.extra = extra
        self.code = code

    def __dict__(self):
        return {'reason': self.reason, 'extra': self.extra}

    def __repr__(self):
        return '<ApiException {!r} {!r} extra:{!r}>'.format(self.code, self.reason, self.extra)

    def to_response(self):
        return jsonify(dict(self)), self.code


class ServerException(ApiException):
    def __init__(self, reason, extra=None):
        super(ServerException, self).__init__(reason, extra=extra, code=500)
