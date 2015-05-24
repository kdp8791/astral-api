from webargs import Arg
from astral.validators.errors import AuthorizationFailed, TokenFailed
from astral.common import constants

def authorize_response_type(response_type):
    if response_type != constants.CODE:
        raise AuthorizationFailed('Invalid response type')

def token_grant_type(grant_type):
    if grant_type != constants.AUTHORIZATION_CODE:
        raise TokenFailed('Invalid grant type')

authorize_args = {
    constants.RESPONSE_TYPE : Arg(str, required=True, validate=authorize_response_type),
    constants.CLIENT_ID : Arg(str, required=True),
    constants.REDIRECT_URI : Arg(str, required=True),
    constants.STATE : Arg(str, required=True)
}

token_args = {
    constants.GRANT_TYPE : Arg(str, required=True, validate=token_grant_type),
    constants.CODE : Arg(str, required=True),
    constants.CLIENT_ID : Arg(str, required=True),
    constants.REDIRECT_URI : Arg(str, required=True),
    constants.CLIENT_SECRET : Arg(str, required=True)
}
