from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

odm_api = Blueprint('odm', __name__, url_prefix='/odm')


@odm_api.route('/get-all', methods=['GET'])
@jwt_required
def get_all():
    return Response(status=501)


@odm_api.route('/get-parameters', methods=['GET'])
@jwt_required
def get_parameters():
    return Response(status=501)
