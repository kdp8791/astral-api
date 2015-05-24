from astral.common import utils, constants, dictionary
import json

def authorization_code(auth, state):
    result = dict()
    result[constants.CLIENT_ID] = auth[constants.CLIENT_ID]
    result[constants.EXP] = utils.five_minute_expire()
    result[constants.STATE] = state
    result[constants.ISS] = dictionary.ISSUER
    return result
