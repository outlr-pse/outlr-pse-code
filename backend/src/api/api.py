"""Defines api endpoint on the main route and manages all sub-routes of the API.

All blueprints from the sub-routes get registered to Flask.
JWT auth is set up with JWTManager.
Defines the /status API endpoint.
The api can be run with the start() method.
"""
from functools import wraps

from flask import Flask, jsonify
from flask.wrappers import Response
from api.experiment_api import experiment_api
from api.user_management_api import user_management_api
from api.odm_api import odm_api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.register_blueprint(experiment_api, url_prefix='/api/experiment')
app.register_blueprint(user_management_api, url_prefix='/api/user')
app.register_blueprint(odm_api, url_prefix='/api/odm')

jwt = JWTManager(app)


@app.route('/api/status', methods=['GET'])
def status() -> Response:
    return jsonify({'status': 'running'})
