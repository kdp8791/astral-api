import string
import urllib
import simplecrypt
import datetime
import time
import jwt
from astral.common import dictionary
from config import enc_key
from urllib.parse import urlparse
from Crypto.Random import random

ASCII_CHARS = (string.ascii_letters + string.digits)

# Encrypt
def encrypt(obj):
    return simplecrypt.encrypt(enc_key, obj)

# Decrypt
def decrypt(obj):
    return simplecrypt.decrypt(enc_key, obj)

def jwt_encode(obj):
    return jwt.encode(obj, enc_key, algorithm='HS256', headers={'typ': 'JWT'})

def jwt_decode(obj):
    return jwt.decode(obj, enc_key, issuer=dictionary.ISSUER, algorithms=['HS256'])

def five_minute_expire():
    return datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

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
