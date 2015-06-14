from astral.common import secrets, utils
import jwt

def build_auth_token(user):
    return (utils.jwt_encode({'email': user['email'], 'exp': utils.one_month_expire()}, secrets.AUTH_JWT)).decode('utf-8')

def generate_confirm_token(email):
    return (utils.jwt_encode({'email': email}, secrets.CONF_JWT)).decode('utf-8')

def decrypt_confirm_token(token):
    return utils.jwt_decode(token, secrets.CONF_JWT)['email']
