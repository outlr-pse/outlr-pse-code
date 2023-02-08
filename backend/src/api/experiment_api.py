"""Defines the experiment API endpoints.

Endpoints defined:
    /validate-dataset
    /validate-ground-truth
    /get-result/<exp_id>
    /get-all
    /create
    /download-result/<exp_id>
"""
import json
from pathlib import Path
from flask import Blueprint, Response, jsonify, send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity

import database.database_access as db
import api.error as error
from init_mock_database import mock_database

experiment_api = Blueprint('experiment', __name__)

# to be deleted
script_location_parent = Path(__file__).absolute().parent

mock_success = True
# when True get_all returns an empty array
no_experiments = False
single_experiment = (not no_experiments) and False

# to be deleted


@experiment_api.route('/validate-dataset', methods=['POST'])
# jwt_required()
def validate_dataset() -> (Response, int):
    """
    Requires a JWT access token. Expects a dataset as a CSV file in the
    request. Returns status code "200 OK" if the dataset was valid, "400
    Bad Request" with message "Invalid dataset." and an error otherwise.
    """
    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        if mock_success:
            return jsonify(message="Valid dataset", status=200)
        return jsonify(error=error.dataset_not_valid), error.dataset_not_valid["status"]
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@experiment_api.route('/validate-ground-truth', methods=['POST'])
# jwt_required()
def validate_ground_truth() -> (Response, int):
    """
    Requires a jwt access token. Expects a ground truth file as a CSV file in
    the request. Returns status code "200 OK" if the ground truth file was
    valid, "400 Bad Request" with message "Invalid dataset." and an error otherwise.
    """
    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        if mock_success:
            return jsonify(message="Valid ground truth", status=200)
        return jsonify(error=error.ground_truth_not_valid), error.ground_truth_not_valid["status"]
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
# jwt_required()
def get_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns status code "200 OK" and the
    experiment results encoded as json. If there is no experiment with the
    given ID it returns "404 Not Found".
    """
    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        if not mock_success:
            return jsonify(error=error.no_experiment_with_id), error.no_experiment_with_id["status"]

        file = open(script_location_parent / 'mock_files/experiment_result.json')
        exp_result = json.load(file)
        response = jsonify(experiment=exp_result, message="Experiment successfully retrieved", status=200)
        return response
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@experiment_api.route('/get-all', methods=['GET'])
# jwt_required()
def get_all() -> list:
    """
    Requires a jwt access token. Returns a list of all experiments the user
    has encoded as json and status code "200 OK". In the case of an error, an is returned with status code
    "400 Bad Request".
    """
    user = db.get_user(get_jwt_identity())
    experiments = user.experiments
    return [e.to_json() for e in experiments]


@experiment_api.route('/create', methods=['POST'])
# jwt_required()
def create() -> (Response, int):
    """
    Requires a jwt access token. Expects an experiment encoded as json in
    the request. Inserts the experiment in the database and runs it. If no experiment was passed, "400 Bad Request"
    and an error is returned
    """
    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        data = request.get_json()
        if not data:
            return jsonify(error=error.no_data_provided), error.no_data_provided["status"]
        if "experiment" not in data:
            return jsonify(error=error.no_experiment_provided), error.no_experiment_provided["status"]

        experiment = data["experiment"]
        if experiment is None:
            return jsonify(error.no_create_experiment_data_provided), error.no_create_experiment_data_provided["status"]
        if not mock_success:
            return jsonify(error.create_experiment_data_not_valid), error.create_experiment_data_not_valid["status"]

        return jsonify(message="Experiment successfully created", status=200)
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
# jwt_required()
def download_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns a CSV file with all the outliers
    from the given experiment and status code "200 OK". If there is no
    experiment with the given ID it returns "404 Not Found".
    """
    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        if not mock_success:
            return jsonify(error=error.no_experiment_with_id), error.no_experiment_with_id["status"]

        return send_file(script_location_parent / "mock_files/outliers.csv", mimetype="text/csv", as_attachment=True)
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]
