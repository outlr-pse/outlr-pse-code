"""Defines the /user API endpoint.

Endpoints defined:
    /user/login
    /user/register
    /user/logout
    /user/check-token
"""

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

user_management_api = Blueprint('user_management', __name__, url_prefix='/user')


@user_management_api.route('/login', methods=['POST'])
def login() -> Response:
    return Response(status=501)


@user_management_api.route('/register', methods=['POST'])
def register() -> Response:
    return Response(status=501)


@user_management_api.route('/logout', methods=['POST'])
@jwt_required()
def logout() -> Response:
    return Response(status=501)


@user_management_api.route('/check-token', methods=['POST'])
@jwt_required()
def check_token() -> Response:
    return Response('Token is valid')
