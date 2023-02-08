"""Defines the experiment API endpoints.

Endpoints defined:
    /validate-dataset
    /validate-ground-truth
    /get-result/<exp_id>
    /get-all
    /create
    /download-result/<exp_id>
"""
import os
from os.path import exists as path_exists

from flask import Blueprint, Response, jsonify, send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.experiment.experiment import Experiment
import database.database_access as db
import util.data as data_utils
import api.error as error

experiment_api = Blueprint('experiment', __name__)


@experiment_api.route('/validate-dataset', methods=['POST'])
@jwt_required()
def validate_dataset() -> (Response, int):
    """
    Requires a JWT access token. Expects a dataset as a CSV file in the
    request. Returns status code "200 OK" if the dataset was valid, "400
    Bad Request" with message "Invalid dataset." and an error otherwise.
    """
    return jsonify(error.not_implemented), error.not_implemented["status"]


@experiment_api.route('/validate-ground-truth', methods=['POST'])
# jwt_required()
def validate_ground_truth() -> (Response, int):
    """
    Requires a jwt access token. Expects a ground truth file as a CSV file in
    the request. Returns status code "200 OK" if the ground truth file was
    valid, "400 Bad Request" with message "Invalid dataset." and an error otherwise.
    """
    return jsonify(error.not_implemented), error.not_implemented["status"]


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def get_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns status code "200 OK" and the
    experiment results encoded as json. If there is no experiment with the
    given ID it returns "404 Not Found".
    """
    user_id = get_jwt_identity()
    exp = db.get_experiment(user_id=user_id, exp_id=exp_id)
    if exp is None:
        return jsonify(error.no_experiment_with_id), error.no_experiment_with_id["status"]
    return exp.to_json(with_outliers=True), 200


@experiment_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> list:
    """
    Requires a jwt access token. Returns a list of all experiments the user
    has encoded as json and status code "200 OK". In the case of an error, an is returned with status code
    "400 Bad Request".
    """
    user = db.get_user(get_jwt_identity())
    experiments = user.experiments
    return [e.to_json(False) for e in experiments]


@experiment_api.route('/count', methods=['GET'])
@jwt_required()
def count() -> (Response, int):
    """
    Requires a jwt access token. Returns the amount of experiments the user
    has and status code "200 OK".
    """
    user = db.get_user(get_jwt_identity())
    amount = len(user.experiments)
    return {"amount": amount}, 200


@experiment_api.route('/upload-files', methods=['POST'])
@jwt_required()
def upload_files() -> (Response, int):
    """
    Requires a jwt access token. Expects a dataset and optionally a ground truth file
    as CSV files in the request. Returns status code "200 OK" if the files
    were valid.
    """
    if "dataset" not in request.files:
        return jsonify(error.no_dataset), error.no_dataset["status"]

    user_id = get_jwt_identity()
    if not os.path.exists(data_path(user_id)):
        os.makedirs(data_path(user_id))

    dataset_file = request.files["dataset"]
    dataset_file.save(data_path(user_id, "dataset"))
    dataset_file.close()

    if "ground_truth" in request.files:
        ground_truth_file = request.files["ground_truth"]
        ground_truth_file.save(data_path(user_id, "ground_truth"))
        ground_truth_file.close()

    return "OK", 200


@experiment_api.route('/create', methods=['POST'])
@jwt_required()
def create() -> (Response, int):
    """
    Requires a jwt access token. Expects an experiment encoded as json in
    the request. Inserts the experiment in the database and runs it. If no experiment was passed, "400 Bad Request"
    and an error is returned
    """
    exp_json = request.json
    user_id = get_jwt_identity()
    exp_json['user_id'] = user_id

    if not path_exists(data_path(user_id, "dataset")):
        return error.no_dataset, error.no_dataset["status"]

    exp = Experiment.from_json(request.json)
    # TODO: remove Dataset class
    exp.dataset = data_utils.csv_to_dataset(exp_json["dataset_name"], data_path(user_id, "dataset"))
    if path_exists(data_path(user_id, "ground_truth")):
        exp.true_outliers = data_utils.csv_to_list(data_path(user_id, "ground_truth"))
    db.add_experiment(exp)
    # TODO: run experiment
    return 'OK', 200


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
# jwt_required()
def download_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns a CSV file with all the outliers
    from the given experiment and status code "200 OK". If there is no
    experiment with the given ID it returns "404 Not Found".
    """
    user_id = 1
    exp = db.get_experiment(user_id=user_id, exp_id=exp_id)
    if exp is None:
        return error.no_experiment_with_id, error.no_experiment_with_id["status"]
    if exp.experiment_result is None:
        return error.experiment_not_run, error.experiment_not_run["status"]

    outliers = [o.index for o in exp.experiment_result.result_space.outliers]
    file = data_utils.write_list_to_csv(outliers)
    return send_file(file, download_name=f'{exp.name}-result.csv', as_attachment=True)


def data_path(user_id: int, file: str = "") -> str:
    base = f"user_data/{user_id}"
    if file == "dataset":
        return f"{base}/dataset.csv"
    elif file == "ground_truth":
        return f"{base}/ground_truth.csv"
    return base
