"""Defines the odm API endpoint.

Endpoints defined:
    /get-all
    /get-parameters/<odm_id>
"""

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

odm_api = Blueprint('odm', __name__)


@odm_api.route('/get-all', methods=['GET'])
@jwt_required()
def get_all() -> Response:
    return Response(status=501)


@odm_api.route('/get-parameters/<int:odm_id>', methods=['GET'])
@jwt_required()
def get_parameters(odm_id: int) -> Response:
    return Response(status=501)
