"""Defines the /experiment API endpoints.

Endpoints defined:
    validate-dataset
    validate-ground-truth
    get-result/<exp_id>
    get-all
    create
    download-result/<exp_id>
"""
import json
from pathlib import Path

from flask import Blueprint, Response, jsonify, send_file, request
from flask_jwt_extended import jwt_required

from backend.src.api.models.error import ExperimentError

experiment_api = Blueprint('experiment', __name__)

# to be deleted
import random
script_location_parent = Path(__file__).absolute().parent

mock_success = True
# when True get_all returns an empty array
no_experiments = False
single_experiment = (not no_experiments) and False

# to be deleted


@experiment_api.route('/validate-dataset', methods=['POST'])
@jwt_required()
def validate_dataset() -> Response:
    """
    Requires a JWT access token. Expects a dataset as a CSV file in the
    request. Returns status code "200 OK" if the dataset was valid, "400
    Bad Request" with message "Invalid dataset." and an ExperimentError otherwise.
    """
    if mock_success:
        return jsonify(message="Valid dataset", status=200)

    dataset_error = ExperimentError("Invalid dataset", 0, 400)
    response = jsonify(message=dataset_error.error_message, status=400, error=dataset_error.to_json())
    response.status = 400
    return response


@experiment_api.route('/validate-ground-truth', methods=['POST'])
@jwt_required()
def validate_ground_truth() -> Response:
    """
    Requires a jwt access token. Expects a ground truth file as a CSV file in
    the request. Returns status code "200 OK" if the ground truth file was
    valid, "400 Bad Request" with message "Invalid dataset." and an ExperimentError otherwise.
    """
    if mock_success:
        return jsonify(message="Valid ground truth", status=200)

    dataset_error = ExperimentError("Invalid dataset", 0, 400)
    response = jsonify(message=dataset_error.error_message, status=400, error=dataset_error.to_json())
    response.status = 400
    return response


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def get_result(exp_id: int) -> Response:
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns status code "200 OK" and the
    experiment results encoded as json. If there is no experiment with the
    given ID it returns "404 Not Found".
    """
    if not mock_success:
        experiment_error = ExperimentError(f'Experiment with {exp_id} as id does not exist', 2, 404)
        response = jsonify(message=experiment_error.error_message, status=404, error=experiment_error.to_json())
        response.status = 404
        return response

    file = open(script_location_parent / 'mock_files/experiment_result.json')
    exp_result = json.load(file)
    response = jsonify(experiment=exp_result, message="Experiment successfully retrieved", status=200)
    return response

@experiment_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> Response:
    """
    Requires a jwt access token. Returns a list of all experiments the user
    has encoded as json and status code "200 OK". In the case of an error, a ODMError is returned with status code
    "400 Bad Request".
    """
    if no_experiments:
        response = jsonify(experiment=[], message="No experiments to be retrieved", status=200)
        return response

    if single_experiment:
        experiment_one = json.load(open(script_location_parent / 'mock_files/experiment_one.json'))
        response = jsonify(experiments=[experiment_one], message="Experiment successfully retrieved", status=200)
        return response

    experiment_one = json.load(open(script_location_parent / 'mock_files/experiment_one.json'))
    experiment_two = json.load(open(script_location_parent / 'mock_files/experiment_two.json'))
    experiments = [experiment_one, experiment_two]
    experiment_array = [experiment_one, experiment_two]

    for i in range(4):
        experiment_array.append(experiments[random.randint(0, 1)])

    response = jsonify(experiments=experiment_array, message="Experiment(s) successfully retrieved", status=200)
    return response


@experiment_api.route('/create', methods=['POST'])
@jwt_required()
def create() -> Response:
    """
    Requires a jwt access token. Expects an experiment encoded as json in
    the request. Inserts the experiment in the database and runs it. If no experiment was passed, "400 Bad Request"
    and an ExperimentError is returned
    """
    experiment = request.json["experiment"]
    if not mock_success or experiment is None:
        create_experiment_error = ExperimentError("Experiment could not be created - something went wrong", 3, 400)
        response = jsonify(message=create_experiment_error.error_message, status=400,
                           error=create_experiment_error.to_json())
        response.status = 400
        return response

    return jsonify(message="Experiment successfully created", status=200)


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def download_result(exp_id: int) -> Response:
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns a CSV file with all the outliers
    from the given experiment and status code "200 OK". If there is no
    experiment with the given ID it returns "404 Not Found".
    """
    if not mock_success:
        download_experiment_result_error = ExperimentError(f'No experiment with {exp_id} to be downloaded', 4, 404)
        response = jsonify(message=download_experiment_result_error.error_message, status=404,
                           error=download_experiment_result_error.to_json())
        response.status = 404
        return response

    return send_file(script_location_parent / "mock_files/outliers.csv", mimetype="text/csv", as_attachment=True)
