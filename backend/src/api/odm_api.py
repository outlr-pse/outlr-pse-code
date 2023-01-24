from flask import Blueprint, Response

odm_api = Blueprint('odm', __name__, url_prefix='/odm')


@odm_api.route('/get-all', methods=['GET'])
def get_all():
    return Response(status=501)


@odm_api.route('/get-parameters', methods=['GET'])
def get_parameters():
    return Response(status=501)
