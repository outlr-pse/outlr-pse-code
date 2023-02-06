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

app = Flask(__name__)
# allows requests from anywhere
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(experiment_api, url_prefix='/api/experiment')
app.register_blueprint(user_management_api, url_prefix='/api/user')
app.register_blueprint(odm_api, url_prefix='/api/odm')

# jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = config.jwt_secret


@app.route('/api/status', methods=['GET'])
def status() -> Response:
    return jsonify({'status': 'running'})
