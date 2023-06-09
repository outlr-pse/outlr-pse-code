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
import concurrent.futures
import datetime

from flask import Blueprint, Response, jsonify, send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from execution.experiment_scheduler.background_thread_event_loop_experiment_scheduler \
    import BackgroundThreadEventLoopExperimentScheduler
from execution.odm_scheduler.executor_odm_scheduler import ExecutorODMScheduler
from models.experiment import Experiment
import database.database_access as db
import util.data as data_utils
import api.error as error
import models.odm

experiment_api = Blueprint('experiment', __name__)

_experiment_scheduler = BackgroundThreadEventLoopExperimentScheduler(
    ExecutorODMScheduler(
        concurrent.futures.ProcessPoolExecutor()
    )
)

_user_files = {
    "dataset": "dataset.csv",
    "ground_truth": "ground_truth.csv"
}


@experiment_api.route('/validate-dataset', methods=['POST'])
@jwt_required()
def validate_dataset() -> (Response, int):
    """
    Requires a JWT access token. Expects a dataset as a CSV file in the
    request. Returns status code "200 OK" if the dataset was valid.
    """
    return jsonify(error.not_implemented), error.not_implemented["status"]


@experiment_api.route('/validate-ground-truth', methods=['POST'])
@jwt_required()
def validate_ground_truth() -> (Response, int):
    """
    Requires a jwt access token. Expects a ground truth file as a CSV file in
    the request. Returns status code "200 OK" if the ground truth file was
    valid.
    """
    return jsonify(error.not_implemented), error.not_implemented["status"]


@experiment_api.route('/get-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def get_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns status code "200 OK" and the
    experiment results encoded as json.
    """
    with db.Session() as session:
        user_id = get_jwt_identity()
        exp = db.get_experiment(session, user_id=user_id, exp_id=exp_id)
        if exp is None:
            return jsonify(error.no_experiment_with_id), error.no_experiment_with_id["status"]
        return exp.to_json(with_outliers=True), 200


@experiment_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> list:
    """
    Requires a jwt access token. Returns a list of all experiments the user
    has encoded as json and status code "200 OK".
    """
    with db.Session() as session:
        user = db.get_user(session, user=get_jwt_identity())
        experiments = user.experiments
        return [e.to_json(False) for e in experiments]


@experiment_api.route('/count', methods=['GET'])
@jwt_required()
def count() -> (Response, int):
    """
    Requires a jwt access token. Returns the amount of experiments the user
    has and status code "200 OK".
    """
    with db.Session() as session:
        user = db.get_user(session, user=get_jwt_identity())
        amount = len(user.experiments)
        return {"amount": amount}, 200


@experiment_api.route('/upload-files', methods=['POST'])
@jwt_required()
def upload_files() -> (Response, int):
    """
    Requires a jwt access token. Expects a dataset and optionally a ground truth file
    as CSV files in the request. Returns status code "200 OK" if the files
    were successfully stored.
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
def create() -> (str, int):
    """
    Requires a jwt access token. Expects an experiment encoded as json in
    the request. Inserts the experiment in the database and runs it.
    """
    with db.Session(expire_on_commit=False) as session:
        # expire_on_commit=False ensures that all the experiment's attributes
        # are still accessible after adding it to the session

        user_id = get_jwt_identity()

        if not path_exists(data_path(user_id, "dataset")):
            return error.no_dataset, error.no_dataset["status"]

        exp = Experiment.from_json(request.json)
        exp.creation_date = datetime.datetime.now()
        exp.user_id = user_id  # User id is not in the json
        db.add_experiment(session, experiment=exp)
        exp.odm.__class__ = models.odm.PyODM  # TODO the ORM should do this automatically in the future

    # Add dataset and optionally ground truth
    exp.dataset = data_utils.csv_to_dataset(data_path(user_id, "dataset"))
    if path_exists(data_path(user_id, "ground_truth")):
        exp.ground_truth = data_utils.csv_to_numpy_array(data_path(user_id, "ground_truth"))

    # Delete the csv files
    remove_user_data(user_id)

    def write_result_to_db(future):
        #  This closure captures exp
        with db.Session() as s:
            s.add(exp)  # Subspace logic does not need to be updated so db.add_experiment is not needed
            s.commit()

    _experiment_scheduler.schedule(exp).add_done_callback(write_result_to_db)

    return 'OK', 200


@experiment_api.route('/download-result/<int:exp_id>', methods=['GET'])
@jwt_required()
def download_result(exp_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects the experiment id in the request.
    If the experiment was found, returns a CSV file with all the outliers
    from the given experiment and status code "200 OK".
    """
    with db.Session() as session:
        user_id = get_jwt_identity()
        exp = db.get_experiment(session, user_id=user_id, exp_id=exp_id)
        if exp is None:
            return error.no_experiment_with_id, error.no_experiment_with_id["status"]
        if exp.experiment_result is None:
            return error.experiment_not_run, error.experiment_not_run["status"]

        outliers = [o.index for o in exp.experiment_result.result_space.outliers]
        file = data_utils.write_list_to_csv(outliers)
        return send_file(file, download_name=f'{exp.name}-result.csv', as_attachment=True)


def data_path(user_id: int, file: str = "") -> str:
    """ Returns the path to the user data directory or a specific file.
    Args:
        user_id: The id of the current user.
        file: The file to return the path to. If empty, the path to the user's data directory is returned.

    Returns:
        The path to the user data directory or a specific file.
    """
    base = f"user_files/{user_id}"
    if file in _user_files:
        return f"{base}/{_user_files[file]}"
    return base


def remove_user_data(user_id: int) -> None:
    """ Removes all data of the user with the given id.
    Args:
        user_id: The id of the user to remove the data of.
    """
    for file, _ in _user_files.items():
        path = data_path(user_id, file)
        if os.path.exists(path):
            os.remove(path)
