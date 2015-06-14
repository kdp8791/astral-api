from webargs import Arg
from astral.common import constants, mongo, bcrypt
from astral.validators.errors import EmailTaken, UnrecognizedUser, UnverifiedUser

def is_email_used(email):
    if mongo.db.users.find_one({'email': email}):
        raise EmailTaken('Email address specified has already been taken.')

def authenticate_validate(email):
    user = mongo.db.users.find_one({'email': email})
    if user is None:
        raise UnrecognizedUser('Email address and/or password provided is not valid.')
    elif user['verified'] is False:
        raise UnverifiedUser('User account must be verified.')

create_args = {
    constants.FIRST_NAME : Arg(str, required=True),
    constants.LAST_NAME : Arg(str, required=True),
    constants.EMAIL : Arg(str, required=True, validate=is_email_used),
    constants.PASSWORD : Arg(str, required=True, validate=lambda p: len(p) > 7),
    constants.PASSWORD_CONF : Arg(str, required=True, validate=lambda p: len(p) > 7),
    constants.CONFIRM_URI : Arg(str, required=True)
}

update_args = {
    constants.PASSWORD : Arg(str, required=False, validate=lambda p: len(p) > 7),
    constants.PASSWORD_CONF : Arg(str, required=False, validate=lambda p: len(p) > 7),
    constants.OLD_PASSWORD : Arg(str, required=False),
    constants.FIRST_NAME : Arg(str, required=False),
    constants.LAST_NAME : Arg(str, required=False)
}

confirm_args = {
    constants.E : Arg(str, required=True)
}

authenticate_args = {
    constants.EMAIL : Arg(str, required=True, validate=authenticate_validate),
    constants.PASSWORD : Arg(str, required=True),
    constants.REMEMBER_ME : Arg(bool, required=False)
}
