import string
import urllib
import simplecrypt
import datetime
import time
import jwt
from astral.common import dictionary
from urllib.parse import urlparse
from Crypto.Random import random

ASCII_CHARS = (string.ascii_letters + string.digits)

def jwt_encode(obj, key):
    obj['iss'] = dictionary.ISSUER
    return jwt.encode(obj, key, algorithm='HS256', headers={'typ': 'JWT'})

def jwt_decode(obj, key):
    return jwt.decode(obj, key, issuer=dictionary.ISSUER, algorithms=['HS256'])

def five_minute_expire():
    return datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

def one_month_expire():
    return datetime.datetime.utcnow() + datetime.timedelta(days=30)

def is_expired(dt):
    print("current_time: {0}, dt: {1}", current_time(), dt)
    return current_time() > dt

def current_time():
    return int(round(time.time()))

def random_string(len):
    return ''.join([random.choice(ASCII_CHARS) for x in xrange(len)])

def isNumeric(obj):
    return obj.isdigit()

def isEmpty(obj):
    if type(obj).__name__ == 'Cursor':
        return obj.count() == 0
    else:
        return obj is None

def mongoObjToStr(obj):
    obj['_id'] = str(obj['_id'])
    return obj
