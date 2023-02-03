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
from flask_jwt_extended import JWTManager
import config

from backend.src.api.models.error import JWTAuthError

app = Flask(__name__)
app.register_blueprint(experiment_api, url_prefix='/api/experiment')
app.register_blueprint(user_management_api, url_prefix='/api/user')
app.register_blueprint(odm_api, url_prefix='/api/odm')

jwt = JWTManager(app)
JWTManager(app)
app.config["JWT_SECRET_KEY"] = config.jwt_secret


@jwt.unauthorized_loader
def unauthorized_token_error(error):
    token_error = JWTAuthError(error, 0, 403)
    response = jsonify(message=error, status=403, error=token_error.to_json())
    response.status = 403
    return response


@jwt.expired_token_loader
def expired_token_error(jwt_header, jwt_payload):
    token_error = JWTAuthError('Token expired', 0, 403)
    response = jsonify(message='Token expired', status=403, error=token_error.to_json())
    response.status = 403
    return response


@jwt.invalid_token_loader
def invalid_token_error(err):
    token_error = JWTAuthError(err, 0, 403)
    response = jsonify(message=err, status=403, error=token_error.to_json())
    response.status = 403
    return response


@jwt.needs_fresh_token_loader
def invalid_token_error(jwt_header, jwt_payload):
    token_error = JWTAuthError('Token declined', 0, 403)
    response = jsonify(message='Token declined', status=403, error=token_error.to_json())
    response.status = 403
    return response


@jwt.revoked_token_loader
def revoked_token_error(jwt_header, jwt_payload):
    token_error = JWTAuthError('Token declined', 0, 403)
    response = jsonify(message='Token declined', status=403, error=token_error.to_json())
    response.status = 403
    return response


@jwt.token_in_blocklist_loader
def blocklist_token_error(jwt_header, jwt_payload):
    blocklist_token_error = JWTAuthError('Token declined', 0, 403)
    response = jsonify(message='Token declined', status=403, error=blocklist_token_error.to_json())
    response.status = 403
    return response


@jwt.token_verification_failed_loader
def verfication_token_error(jwt_header, jwt_payload):
    verfication_token_error = JWTAuthError('Token declined', 0, 403)
    response = jsonify(message='Token declined', status=403, error=verfication_token_error.to_json())
    response.status = 403
    return response


@app.route('/api/status', methods=['GET'])
def status() -> Response:
    return jsonify({'status': 'running'})
