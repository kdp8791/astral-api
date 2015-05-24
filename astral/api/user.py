from astral.common import constants, utils
import flask

user_api = flask.Blueprint('user_api', __name__)

@user_api.route('/api/v1.0/login', methods=['POST'])
def login():
    if constants.EMAIL in session:
        return flask.jsonify(success=True)
    else:
        return flask.jsonify(loggedIn=False)
