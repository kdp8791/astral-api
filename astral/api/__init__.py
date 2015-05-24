import os
import logging
from flask import Flask, jsonify
import config
from astral.api.oauth import oauth_api
from astral.api.user import user_api
from astral.common import mongo
from astral.validators.errors import AstralException

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
mongo.init_app(app)

app.register_blueprint(oauth_api)
app.register_blueprint(user_api)

file_handler = logging.FileHandler(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "log", "root.log")))
if not app.debug:
	file_handler.setLevel(logging.WARNING)
else:
	file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

@app.errorhandler(AstralException)
def handle(err):
	response = jsonify(getattr(err, 'response'))
	return response

@app.errorhandler(400)
def handle_bad_request(err):
	data = getattr(err, 'data')
	if data:
		msg = data['message']
		error_type = data['exc'].__class__.__name__
	else:
		msg = 'Invalid request'
		error_type = 'UnknownErrorType'
	return jsonify(status_code=400, message=msg, type=error_type)
