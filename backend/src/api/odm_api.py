"""Defines the odm API endpoint.

Endpoints defined:
    /get-all
    /get-parameters/<odm_id>
"""
import json
import random
from pathlib import Path

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

from backend.src.api.models import error
from backend.src.api.user_management_api import mock_jwt_required

odm_api = Blueprint('odm', __name__)
# to be deleted
mock_success = True
script_location_parent = Path(__file__).absolute().parent
single_odm = True
# to be deleted


@odm_api.route('/get-all', methods=['GET'])
@mock_jwt_required()
def get_all() -> (Response, int):
    """
    Requires a jwt access token. Returns a list of all ODMs available to the
    user encoded as json and status code "200 OK". In the case of an error, an error is returned with status code
    "400 Bad Request".
    """
    if not mock_success:
        return jsonify(error.error_other), error.error_other["status"]

    if single_odm:
        odm_one = json.load(open(script_location_parent / 'mock_files/odm_one.json'))
        response = jsonify(odms=[odm_one], message="ODM successfully retrieved")
        return response

    odm_one = json.load(open(script_location_parent / 'mock_files/odm_one.json'))
    odm_two = json.load(open(script_location_parent / 'mock_files/odm_two.json'))

    odms = [odm_one, odm_two]
    odms_array = [odm_one, odm_two]

    for i in range(15):
        odms_array.append(odms[random.randint(0, 1)])

    response = jsonify(odms=odms_array, message="ODMs successfully retrieved", status=200)
    return response


@odm_api.route('/get-parameters/<int:odm_id>', methods=['GET'])
@mock_jwt_required()
def get_parameters(odm_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects an ODM id. Returns a list of all
    parameters the given ODM has encoded as json and status code "200
    OK" if the ODM was found, status code "400 Bad Request" and ODMError otherwise.
    """
    if not mock_success:
        return jsonify(error.no_odm_with_id), error.no_odm_with_id["status"]

    hyperparams = json.load(open(script_location_parent / 'mock_files/hyperparameters.json'))
    response = jsonify(hyperparameters=hyperparams, message="Hyperparameters successfully retrieved", status=200)
    return response
