from pymongo import MongoClient
from astral.config import config
import os

class AstralDB(object):

	def __init__(self, app=None):
		env = os.getenv('ENV')
		client = MongoClient(config.get(env, 'host'), int(config.get(env, 'port')))
		self._db = client[config.get(env, 'database')]
		self._db.authenticate(config.get(env, 'user'), config.get(env, 'password'))
		if app != None:
			app.logger.info(config.get(env, 'host') + " connected")

	def get_connection():
		return self._db
