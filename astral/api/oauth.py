from astral.common import constants, utils, mongo
from astral.models import oauth
from astral.validators.errors import AuthorizationFailed
from astral.validators.oauth import *
from webargs.flaskparser import use_kwargs
from flask import Blueprint, jsonify
from bson.objectid import ObjectId

oauth_api = Blueprint('oauth_api', __name__)

@oauth_api.route('/api/v1.0/oauth/authorize', methods=['GET'])
@use_kwargs(authorize_args)
def authorize(response_type, client_id, redirect_uri, state):
    auth = mongo.db.oauths.find_one({'client_id': client_id})
    if utils.isEmpty(auth):
        raise AuthorizationFailed('Invalid request parameters for authorization.')
    elif redirect_uri.lower() not in auth['redirect_uri']:
        raise AuthorizationFailed('The redirect uri specified is not configured with this app.')
    else:
        message = oauth.authorization_code(auth, state)
        code = utils.jwt_encode(message)
        return jsonify(code=str(code))

@oauth_api.route('/api/v1.0/oauth/token', methods=['POST'])
@use_kwargs(token_args)
def token(grant_type, code, redirect_uri, client_id, client_secret):
    message = utils.jwt_decode(bytes(str.encode(code), 'utf-8'))
    return jsonify(code=message)
