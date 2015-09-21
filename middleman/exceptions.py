# -*- coding: utf-8 -*-
from flask import jsonify


class ApiException(Exception):
    def __init__(self, reason=None, extra=None, code=409):
        Exception.__init__(self)

        self.reason = reason
        self.extra = extra
        self.code = code

    def __repr__(self):
        return '<ApiException {!r} {!r} extra:{!r}>'.format(self.code, self.reason, self.extra)

    def to_response(self):
        response = jsonify({'reason': self.reason, 'extra': self.extra})
        response.status_code = self.code

        return response


class ServerException(ApiException):
    def __init__(self, reason, extra=None):
        super(ServerException, self).__init__(reason, extra=extra, code=500)
