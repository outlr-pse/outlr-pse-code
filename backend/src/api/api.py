"""Defines api endpoint on the main route and manages all sub-routes of the API.

All blueprints from the sub-routes get registered to Flask.
JWT auth is set up with JWTManager.
Defines the /status API endpoint.
The api can be run with the start() method.
"""

from flask import Flask, jsonify
from flask.wrappers import Response
from api.experiment_api import experiment_api
from api.user_management_api import user_management_api
from api.odm_api import odm_api
from flask_cors import CORS
import config
from flask_jwt_extended import JWTManager
from api import error

app = Flask(__name__)
# allows requests from anywhere
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(experiment_api, url_prefix='/api/experiment')
app.register_blueprint(user_management_api, url_prefix='/api/user')
app.register_blueprint(odm_api, url_prefix='/api/odm')
app.config["JWT_SECRET_KEY"] = config.jwt_secret
jwt = JWTManager(app)


@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


@jwt.unauthorized_loader
def unauthorized_token_callback(reason):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


@jwt.expired_token_loader
def expired_token_callback(header, payload):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


@jwt.token_in_blocklist_loader
def token_blocked_callback(header, payload):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


@jwt.token_verification_failed_loader
def token_verification_failed_callback(header, payload):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


@jwt.user_lookup_error_loader
def user_lookup_error_callback(header, payload):
    return jsonify(error=error.user_look_up_failed), error.user_look_up_failed["status"]


@jwt.revoked_token_loader
def token_revoked_callback(header, payload):
    return jsonify(error=error.token_not_valid), error.token_not_valid["status"]


# ENDPOINTS
@app.route('/api/status', methods=['GET'])
def status() -> Response:
    return jsonify({'status': 'running'})

