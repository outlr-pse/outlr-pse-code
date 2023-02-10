"""Defines the odm API endpoint.

Endpoints defined:
    /get-all
    /get-parameters/<odm_id>
"""
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

import api.error as error
import database.database_access as db

odm_api = Blueprint('odm', __name__)


@odm_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> (Response, int):
    """
    Requires a jwt access token. Returns a list of all ODMs available to the
    user encoded as json and status code "200 OK". If no ODMs were found, returns status 404 "Not Found"
    and error "no_odms_found".
    """
    all_odms: list[dict] = [odm.to_json_no_params() for odm in db.get_all_odms()]
    if not all_odms:
        return jsonify(error.no_odms_found), 404

    response = jsonify(all_odms)
    return response, 200


@odm_api.route('/get-parameters/<int:odm_id>', methods=['GET'])
@jwt_required()
def get_parameters(odm_id: int) -> (Response, int):
    """
    Requires a jwt access token. Expects an ODM id. Returns a list of all
    parameters the given ODM has, encoded as json and with status code "200
    OK" if the ODM was found.
    If no such odm was found, returns status 404 "Not Found" and error "no_such_odm".
    """
    odm = db.get_odm(odm_id)
    if not odm:
        return jsonify(error.no_such_odm), 404

    response = jsonify([param.to_json() for param in odm.hyper_parameters])
    return response, 200
