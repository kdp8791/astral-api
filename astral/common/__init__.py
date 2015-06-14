from flask import request, _request_ctx_stack
from werkzeug.local import LocalProxy
from flask.ext.pymongo import PyMongo
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from functools import wraps
from astral.common import secrets, utils
from astral.validators.errors import UnauthorizedAccess, InvalidAuthorizationToken, ExpiredAuthorizationToken

mongo = PyMongo()
bcrypt = Bcrypt()
mail = Mail()

current_user = LocalProxy(lambda: _request_ctx_stack.top.current_user)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise UnauthorizedAccess('Missing authentication tokens.')
        auth = request.headers['Authorization']
        if not auth:
            raise UnauthorizedAccess('Authentication not granted for accessing this resource.')
        auth = auth.split()
        if auth[0].lower() != 'bearer' or len(auth) == 1 or len(auth) > 2:
            raise UnauthorizedAccess('Authentication not granted for accessing this resource.')
        auth = auth[1]
        token = None
        try:
            token = utils.jwt_decode(auth, secrets.AUTH_JWT)
        except Exception as e:
            raise InvalidAuthorizationToken('Authentication token could not be validated.')
        user = mongo.db.users.find_one({'email': token['email']})
        _request_ctx_stack.top.current_user = user
        return f(*args, **kwargs)

    return decorated
