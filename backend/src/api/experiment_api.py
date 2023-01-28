"""Defines the /experiment API endpoints.

Endpoints defined:
    /experiment/validate-dataset
    /experiment/validate-ground-truth
    /experiment/get-result/<exp_id>
    /experiment/get-all
    /experiment/create
    /experiment/download-result/<exp_id>
"""
import json
from pathlib import Path

from flask import Blueprint, Response, jsonify, send_file
from flask_jwt_extended import jwt_required
experiment_api = Blueprint('experiment', __name__, url_prefix='/experiment')

#to be deleted
import random
script_location_parent = Path(__file__).absolute().parent

mock_success = True
# when True get_all returns an empty array
no_experiments = False
single_experiment = (not no_experiments) and False

#to be deleted

@experiment_api.route('/validate-dataset', methods=['POST'])
#@jwt_required()
def validate_dataset() -> Response:
    if mock_success:
        return jsonify(message="Valid dataset", status=200)

    no_success_response = jsonify(message="Invalid dataset", status=400)
    no_success_response.status = 400
    return no_success_response

@experiment_api.route('/validate-ground-truth', methods=['POST'])
#@jwt_required()
def validate_ground_truth() -> Response:
    if mock_success:
        return jsonify(message="Valid ground truth", status=200)

    no_success_response = jsonify(message="Invalid dataset", status=400)
    no_success_response.status = 400
    return no_success_response


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
#@jwt_required()
def get_result(exp_id: int) -> Response:
    if not mock_success:
        no_success_response = jsonify(message="Experiment with provided id does not exist", status=404)
        no_success_response.status = 404
        return no_success_response

    file = open(script_location_parent / 'mock_files/experiment_result.json')
    exp_result = json.load(file)
    response = jsonify(experiment=exp_result, message="Experiment successfully retrieved", status=200)
    return response

@experiment_api.route('/get-all', methods=['GET'])
#@jwt_required()
def get_all() -> Response:
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
#@jwt_required()
def create() -> Response:
    if not mock_success:
        no_success_response = jsonify(message="Experiment could not be created - something went wrong", status=400)
        no_success_response.status = 400
        return no_success_response

    return jsonify(message="Experiment successfully created", status=200)

@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
#@jwt_required()
def download_result(exp_id: int) -> Response:
    if not mock_success:
        no_success_response = jsonify(message="Experiment result could not be download - not found", status=404)
        no_success_response.status = 404
        return no_success_response

    return send_file(script_location_parent / "mock_files/outliers.csv", mimetype="text/csv", as_attachment=True)
