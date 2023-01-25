from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

user_management_api = Blueprint('user_management', __name__, url_prefix='/user')


@user_management_api.route('/login', methods=['POST'])
def login():
    return Response(status=501)


@user_management_api.route('/register', methods=['POST'])
def register():
    return Response(status=501)


@user_management_api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return Response(status=501)


@user_management_api.route('/check_token', methods=['POST'])
@jwt_required()
def check_token():
    return 'Token is valid'
