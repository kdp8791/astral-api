import os
import logging
import flask
from astral.config import config
from astral.db import AstralDB

app = flask.Flask(__name__)
app.secret_key = config.get('app', 'secret_key')
mongo = AstralDB(app)

file_handler = logging.FileHandler(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "log", "astral.log")))
if not app.debug:
	file_handler.setLevel(logging.WARNING)
else:
	file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)