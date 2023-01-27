"""Defines the /experiment API endpoints.

Endpoints defined:
    /experiment/validate-dataset
    /experiment/validate-ground-truth
    /experiment/get-result/<exp_id>
    /experiment/get-all
    /experiment/create
    /experiment/download-result/<exp_id>
"""

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

from api.api import mock_jwt_required

experiment_api = Blueprint('experiment', __name__, url_prefix='/experiment')
mock_success = True

@experiment_api.route('/validate-dataset', methods=['POST'])
@mock_jwt_required()
def validate_dataset() -> Response:
    if mock_success:
        return jsonify(status=200)

    no_success_response = jsonify(message="Invalid dataset", status=400)
    no_success_response.status = 400
    return no_success_response

@experiment_api.route('/validate-ground-truth', methods=['POST'])
@mock_jwt_required()
def validate_ground_truth() -> Response:
    if mock_success:
        return jsonify(status=200)

    no_success_response = jsonify(message="Invalid dataset", status=400)
    no_success_response.status = 400
    return no_success_response


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
@mock_jwt_required()
def get_result(exp_id: int) -> Response:
    return Response(status=501)



@experiment_api.route('/get-all', methods=['GET'])
@mock_jwt_required()
def get_all() -> Response:
    return Response(status=501)


@experiment_api.route('/create', methods=['POST'])
@mock_jwt_required()
def create() -> Response:
    return Response(status=501)


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
@mock_jwt_required()
def download_result(exp_id: int) -> Response:
    return Response(status=501)
