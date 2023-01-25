from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

experiment_api = Blueprint('experiment', __name__, url_prefix='/experiment')


@experiment_api.route('/validate-dataset', methods=['POST'])
@jwt_required()
def validate_dataset():
    return Response(status=501)


@experiment_api.route('/validate-ground-truth', methods=['POST'])
@jwt_required()
def validate_ground_truth():
    return Response(status=501)


@experiment_api.route('/get-result', methods=['GET'])
@jwt_required()
def get_result():
    return Response(status=501)


@experiment_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all():
    return Response(status=501)


@experiment_api.route('/create', methods=['POST'])
@jwt_required()
def create():
    return Response(status=501)


@experiment_api.route('/download-result', methods=['GET'])
@jwt_required()
def download_result():
    return Response(status=501)
