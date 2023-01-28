"""Defines the /odm API endpoint.

Endpoints defined:
    /odm/get-all
    /odm/get-parameters/<odm_id>
"""
import json
import random
from pathlib import Path

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

odm_api = Blueprint('odm', __name__, url_prefix='/odm')
mock_success = True
script_location_parent = Path(__file__).absolute().parent
single_odm = True

@odm_api.route('/get-all', methods=['GET'])
#@jwt_required()
def get_all() -> Response:
    if not mock_success:
        no_success_response = jsonify(message="Something went wrong", status=400)
        no_success_response.status = 400
        return no_success_response

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
#mock_jwt_required()
def get_parameters(odm_id: int) -> Response:
    if not mock_success:
        no_success_response = jsonify(message="ODM not found", status=400)
        no_success_response.status = 400
        return no_success_response

    hyperparams = json.load(open(script_location_parent / 'mock_files/hyperparameters.json'))
    response = jsonify(hyperparameters=hyperparams, message="Hyperparameters successfully retrieved", status=200)
    return response
