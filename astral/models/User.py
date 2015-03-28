from mongokit import *
import datetime
import re
from astral.api import connection

def email_validator(value):
	email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',re.IGNORECASE)
	is_valid = bool(email.match(value))
	if not is_valid:
		raise ValidationError("%s is not a valid email")
	return is_valid

@connection.register
class User(Document):

	structure = {
		'first_name': unicode,
		'last_name': unicode,
		'email': unicode,
		'password': unicode,
		'create_date': datetime.datetime,
		'last_activity_date': datetime.datetime,
		'status': unicode,
		'is_confirmed': bool
	}

	required = ['first_name', 'last_name', 'email', 'password']

	validators = {
		'email': email_validator
	}

	use_dot_notation = True

	def __repr__(self):
		return '<User %r>' % (self.email)