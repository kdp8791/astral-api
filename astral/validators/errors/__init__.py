from flask import jsonify

class AstralException(Exception):

    def __init__(self, message, status_code, class_type):
        Exception.__init__(self)
        self.response = dict()
        self.response['message'] = message
        self.response['status_code'] = status_code
        self.response['type'] = class_type

    def __rep__(self):
        return 'AstralException({0!r}, status_code={1})'.format(self.message, self.status_code)

# GeneralServerError exception
class GeneralServerException(AstralException):
    status_code = 500
    message = 'A general server error was encountered while trying to process your request.'

    def __init__(self, class_type=None, message=None):
        if message is not None:
            self.message = message
        AstralException.__init__(self, self.message, self.status_code, type(self).__name__ if class_type is None else class_type)

# BadRequest exception
class BadRequestException(AstralException):
    status_code = 400
    message = 'The requested resource is either not a valid resource or available at this moment.'

    def __init__(self, class_type=None, message=None):
        if message is not None:
            self.message = message
        AstralException.__init__(self, self.message, self.status_code, type(self).__name__ if class_type is None else class_type)

# NotFound exception
class NotFoundException(AstralException):
    status_code = 404
    message = 'The requested resource is not available.'

    def __init__(self, class_type=None, message=None):
        if message is not None:
            self.message = message
        AstralException.__init__(self, self.message, self.status_code, type(self).__name__ if class_type is None else class_type)

# Found exception
class FoundException(AstralException):
    status_code = 302
    message = 'The request resource was found, but an error occurred when trying to process your request.'

    def __init__(self, class_type=None, message=None):
        if message is not None:
            self.message = message
        AstralException.__init__(self, self.message, self.status_code, type(self).__name__ if class_type is None else class_type)

# GeneralServerError exception
class GeneralServerException(AstralException):
    status_code = 500
    message = 'A general server error was encountered while trying to process your request.'

    def __init__(self, class_type=None, message=None):
        if message is not None:
            self.message = message
        AstralException.__init__(self, self.message, self.status_code, type(self).__name__ if class_type is None else class_type)

class AuthorizationFailed(BadRequestException):

    def __init__(self, message):
        BadRequestException.__init__(self, type(self).__name__, message)

class TokenFailed(BadRequestException):

    def __init__(self, message):
        BadRequestException.__init__(self, type(self).__name__, message)
