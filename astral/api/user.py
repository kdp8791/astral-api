from astral.common import *
from flask import Blueprint, jsonify, redirect, make_response
from webargs.flaskparser import use_args
from astral.validators.errors import *
from astral.validators.user import *
from astral.models import users
from flask.ext.mail import Message
import logging

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/v1.0/user/create', methods=['POST'])
@use_args(create_args)
def create(args):
    if args[constants.PASSWORD] != args[constants.PASSWORD_CONF]:
        raise PasswordMismatch('Passwords provided do not match.')
    else:
        url = mongo.db.sources.find_one({'name': args[constants.CONFIRM_URI]})
        if url is None:
            raise InvalidConfirmationUri('Invalid confirmation uri')
        mongo.db.users.insert(
        {
            'firstName': args[constants.FIRST_NAME],
            'lastName': args[constants.LAST_NAME],
            'email': args[constants.EMAIL],
            'password': bcrypt.generate_password_hash(args[constants.PASSWORD], 12),
            'verified': False,
            'email_blocked': False,
            'status': constants.PENDING
        })
        try:
            url = '{0}?e={1}'.format(url['uri'], users.generate_confirm_token(args[constants.EMAIL]))
            template = mongo.db.emailtemplates.find_one({'type': 'confirm'})
            msg = Message(template['subject'], recipients=[args[constants.EMAIL]])
            msg.body = template['body'].format(args[constants.FIRST_NAME], args[constants.LAST_NAME], url)
            msg.html = template['html'].format(args[constants.FIRST_NAME], args[constants.LAST_NAME], url)
            mail.send(msg)
            return jsonify(created=True)
        except Exception:
            return jsonify(created=False)

@user_api.route('/api/v1.0/user/update', methods=['POST'])
@use_args(update_args)
@requires_auth
def update(args):
    if args[constants.FIRST_NAME] is not None:
        current_user['firstName'] = args[constants.FIRST_NAME]
    if args[constants.LAST_NAME] is not None:
        current_user['lastName'] = args[constants.LAST_NAME]
    if args[constants.PASSWORD] is not None and args[constants.PASSWORD_CONF] is None:
        raise BadRequest('Missing confirmation password.')
    elif args[constants.PASSWORD] is not None and args[constants.PASSWORD_CONF] is not None and args[constants.OLD_PASSWORD] is None:
        raise BadRequest('Missing old password.')
    if args[constants.PASSWORD] is not None and args[constants.OLD_PASSWORD] is not None:
        if args[constants.PASSWORD] != args[constants.PASSWORD_CONF]:
            raise PasswordMismatch('Password provided do not match.')
        elif args[constants.OLD_PASSWORD] is not None:
            if bcrypt.generate_password_hash(args[constants.OLD_PASSWORD], 12) == current_user['password']:
                current_user['password'] = bcrypt.generate_password_hash(args[constants.PASSWORD], 12)
            else:
                raise BadRequest('User account is not valid.')
    print(current_user)
    mongo.db.users.update({'_id': current_user['_id']}, {'$set': current_user}, upsert=False)
    return jsonify(updated=True)

@user_api.route('/api/v1.0/user/confirm', methods=['GET'])
@use_args(confirm_args)
def confirm(args):
    if mongo.db.conf_tokens_used.find_one({'token': args[constants.E]}) is not None:
        raise ConfirmationUsed('The confirmation token provided has already been used.')
    else:
        token = None
        try:
            token = users.decrypt_confirm_token(args[constants.E])
        except Exception as e:
            raise InvalidConfirmationToken('Confirmation token provided is not valid.')
        user = mongo.db.users.find_one({'email': token})
        if user['verified'] is False:
            user['status'] = constants.ACTIVE
            user['verified'] = True
            mongo.db.users.update({'_id': user['_id']}, {'$set': user}, upsert=False)
            return jsonify(confirmed=True)
        else:
            raise AlreadyConfirmedUser('Account has already been confirmed.')

@user_api.route('/api/v1.0/user/authenticate', methods=['POST'])
@use_args(authenticate_args)
def authenticate(args):
    user = mongo.db.users.find_one({'email': args[constants.EMAIL]})
    if bcrypt.check_password_hash(user[constants.PASSWORD], args[constants.PASSWORD]) is True:
        token = users.build_auth_token(user)
        resp = make_response()
        resp.headers['Authorization'] = "Bearer {0}".format(token)
        return resp
    else:
        raise UnrecognizedUser('Email address and/or password provided is not valid.')
