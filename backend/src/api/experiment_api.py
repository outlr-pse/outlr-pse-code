"""Defines the experiment API endpoints.

Endpoints defined:
    /validate-dataset
    /validate-ground-truth
    /get-result/<exp_id>
    /get-all
    /create
    /download-result/<exp_id>
"""

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

experiment_api = Blueprint('experiment', __name__)


@experiment_api.route('/validate-dataset', methods=['POST'])
@jwt_required()
def validate_dataset() -> Response:
    return Response(status=501)


@experiment_api.route('/validate-ground-truth', methods=['POST'])
@jwt_required()
def validate_ground_truth() -> Response:
    return Response(status=501)


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def get_result(exp_id: int) -> Response:
    return Response(status=501)


@experiment_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> Response:
    return Response(status=501)


@experiment_api.route('/create', methods=['POST'])
@jwt_required()
def create() -> Response:
    return Response(status=501)


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def download_result(exp_id: int) -> Response:
    return Response(status=501)
