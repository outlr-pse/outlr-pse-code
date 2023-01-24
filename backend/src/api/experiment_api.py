from flask import Blueprint, Response

experiment_api = Blueprint('experiment', __name__, url_prefix='/experiment')


@experiment_api.route('/validate-dataset', methods=['GET'])
def validate_dataset():
    return Response(status=501)


@experiment_api.route('/validate-ground-truth', methods=['GET'])
def validate_ground_truth():
    return Response(status=501)


@experiment_api.route('/get-result', methods=['GET'])
def get_result():
    return Response(status=501)


@experiment_api.route('/get-all', methods=['GET'])
def get_all():
    return Response(status=501)


@experiment_api.route('/create', methods=['GET'])
def create():
    return Response(status=501)


@experiment_api.route('/download-result', methods=['GET'])
def download_result():
    return Response(status=501)
