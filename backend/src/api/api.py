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

app = Flask(__name__)
app.register_blueprint(experiment_api)
app.register_blueprint(user_management_api)
app.register_blueprint(odm_api)

JWTManager(app)


@app.route('/status', methods=['GET'])
def status() -> Response:
    return jsonify({'status': 'running'})


def start() -> None:
    """Starts the API.

    Currently on localhost port 5000 in debug mode. Will be changed in the future.
    """
    # todo: change host, debug (and port if necessary)
    app.run(host='localhost', port=5000, debug=True)
